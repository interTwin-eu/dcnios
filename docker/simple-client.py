#!/usr/bin/env python3
"""test application to demonstrate dCache inotify"""
from sseclient import SSEClient
import requests
import urllib3
import getpass
import argparse
import json
import activities
import liboidcagent as oidc
import os
import uuid
import time
import calendar
##
##  This util needs liboidcagent, which may be installed via
##
##      pip install liboidcagent
##
##  or
##
##      pip3 install liboidcagent
##

workfolder="/state"

class OidcAuth(requests.auth.AuthBase):
    """Support for authenticating with OIDC access token"""
    def __init__(self, account):
        self.account = account

    def __call__(self, r):
        token = oidc.get_access_token(self.account)
        r.headers.update({'Authorization': "Bearer %s" % (token)})
        return r

parser = argparse.ArgumentParser(description='Sample dCache SSE consumer')
parser.add_argument('--state', metavar="PATH",
                    help='Path of a file in which information is stored to avoid loosing events.')
parser.add_argument('--endpoint',
                    default="https://prometheus.desy.de:3880/api/v1",
                    help="The events endpoint.  This should be a URL like 'https://frontend.example.org:3880/api/v1'.")
parser.add_argument('--auth', metavar="METHOD", choices=['userpw', 'x509', 'oidc'], default="userpw",
                    help="How to authenticate.")
parser.add_argument('--user', metavar="NAME", default=getpass.getuser(),
                    help="The dCache username.  Defaults to the current user's name.")
parser.add_argument('--oidc-account', metavar="NAME", help="The oidc-agent account name")
parser.add_argument('--recursive', '-r', action='store_const', const='recursive', default='single')
parser.add_argument('--password', default=None,
                    help="The dCache password.  Defaults to prompting the user.")
parser.add_argument('--x509-trust', choices=['path', 'builtin', 'any'],
                    help="Which certificate authorities to trust when checking a server certificate.",
                    default='builtin')
parser.add_argument('--x509-trust-path', metavar="PATH", default='/etc/grid-security/certificates',
                    help="Trust anchor location if --x509-trust is 'path'.")
parser.add_argument('--x509-proxy', metavar="PATH", dest='proxy',
                    default=os.environ.get('X509_USER_PROXY', '/tmp/x509up_u' + str(os.getuid())),
                    help='Client X509 proxy file.')
parser.add_argument('paths', metavar='PATH', nargs='+',
                    help='The paths to watch.')
parser.add_argument('--activity', metavar="ACTIVITY", choices=['print', 'unarchive', 'execute'], default="print",
                    help='What to do with the inotify events.')
parser.add_argument('--target-path', metavar="PATH", default=None, help="The path for unarchive activity");
parser.add_argument('--execute-command', metavar="CMD", default=None, help="Command to execute");
args = vars(parser.parse_args())

state_path = args["state"]
auth = args["auth"]
user = args["user"]
pw = args["password"]
oidc_account = args["oidc_account"]
isRecursive = args["recursive"] == 'recursive'
if auth == 'userpw' and not pw:
    pw = getpass.getpass("Please enter dCache password for user " + user + ": ")
    args["password"] = pw
if auth == 'oidc' and not oidc_account:
    raise Exception('Missing oidc-agent account name.  Please specify --oidc-account')

def configure_session(args):
    s = requests.Session()

    auth = args.get("auth")
    if auth == 'userpw':
        s.auth = (args.get("user"),args.get("password"))
    elif auth == 'oidc':
        s.auth = OidcAuth(oidc_account)
    else:
        s.cert = args.get("proxy")

    trust = args["x509_trust"]
    if trust == 'any':
        print("Disabling certificate verification: connection is insecure!")
        s.verify = False
        urllib3.disable_warnings()
    elif trust == 'path':
        s.verify = args.get("x509-trust-path")
    elif trust != 'builtin':
        raise Exception('Unknown trust value: ' + str(trust))
    return s

def request_channel(session):
    print("Creating a new channel")
    response = session.post(args["endpoint"] + '/events/channels')
    response.raise_for_status()
    return response.headers['Location']

eventCount = 0
activity_name = args.get("activity")

if activity_name == 'print':
    activity = activities.PrintActivity()
elif activity_name == 'unarchive':
    target = args.get("target_path")
    if not target:
        raise Exception('Missing --target-path argument')
    activity = activities.UnarchiveActivity(target, args=args, session_factory=configure_session, api_url=args["endpoint"])
elif activity_name == 'execute':
    cmd = args.get("execute_command")
    if not cmd:
        raise Exception('Missing --execute-command argument')
    activity = activities.ExecuteActivity(cmd)
else:
    raise Exception('Unknown activity: ' + activity)

def watch(channel, path):
    "Add a watch and update watches list if successful"
    w = s.post(format(channel) + "/subscriptions/inotify",
               json={"path": path, "flags": ["IN_CLOSE_WRITE", "IN_CREATE",
                                             "IN_DELETE", "IN_DELETE_SELF",
                                             "IN_MOVE_SELF", "IN_MOVE",
                                             "IN_ATTRIB"]})
    w.raise_for_status()
    watch = w.headers['Location']
    print("Watching %s" % path)
    watches[watch] = path

def single_watch(channel, path):
    "Watch a single path (i.e., non-recursive)"
    try:
        watch(channel, path)
    except requests.exceptions.HTTPError as e:
        r = e.response
        if r.status_code == 400:
            print("Watch for path %s request failed: %s" % (path, r.json()["errors"][0]["message"]))
        else:
            print("Server rejected watch for path %s: %s" % (path, str(e)))

    except requests.exceptions.RequestException as e:
        print("Failed to watch path %s: %s" % (path, str(e)))


def watch_subdirectories(path):
    "Recursively watch all subdirectories of the given path"
    try:
        r = s.get(args["endpoint"] + "/namespace" + path + "?children=true")
        r.raise_for_status()
        dir_list = r.json()
        children = dir_list["children"]

        for item in children:
            if item["fileType"] == "DIR":
                recursive_watch(channel, path + "/" + item["fileName"])

    except requests.exceptions.HTTPError as e:
        r = e.response
        if r.status_code == 400:
            print("Directory listing for path %s failed: %s" % (path, r.json()["errors"][0]["message"]))
        else:
            print("Server rejected directory listing for path %s: %s" % (path, str(e)))

    except requests.exceptions.RequestException as e:
        print("Failed to list directory %s: %s" % (path, str(e)))


def recursive_watch(channel, path):
    "Watch path and any subdirectories, recursively"
    try:
        watch(channel, path)
        watch_subdirectories(path)

    except requests.exceptions.HTTPError as e:
        r = e.response
        if r.status_code == 400:
            print("Watch for path %s request failed: %s" % (path, r.json()["errors"][0]["message"]))
        else:
            print("Server rejected watch for path %s: %s" % (path, str(e)))

    except requests.exceptions.RequestException as e:
        print("Failed to watch path %s: %s" % (path, str(e)))



def checkMoveEvents():
    pop_list = []
    for cookie, (path, action, removeAt) in mvCookie.items():
        if removeAt <= eventCount:
            pop_list.append(cookie)

    for c in pop_list:
        (path,action,_) = mvCookie.pop(c)
        if action == 'IN_MOVE_FROM':
            activity.onDeletedFile(path)
        else:
            activity.onNewFile(path)


def inotify(type, sub, event,msg):
    mask = event['mask']
    if 'name' in event:
        path = watches[sub] + '/' + event['name']
    else:
        path = watches[sub]
        if path in paths and isRecursive:
            return

    isDir = False
    for flag in mask:
        if flag == 'IN_ISDIR':
            isDir = True
        else:
            action = flag

    if action == 'IN_CREATE' and isDir and isRecursive:
        single_watch(channel, path)

    if action == 'IN_IGNORED' and isDir:
        watches.pop(path)

    if action == 'IN_MOVED_FROM':
        mvFrom = path
        cookie = event['cookie']
        if cookie in mvCookie:
            (mvTo, _, _) = mvCookie[cookie]
            del mvCookie[cookie]
            if isDir:
                activity.onMovedDirectory(mvFrom, mvTo)
            else:
                activity.onMovedFile(mvFrom, mvTo)
        else:
            mvCookie[cookie] = (path,action, eventCount+5)

    elif action == 'IN_MOVED_TO':
        mvTo = path
        cookie = event['cookie']
        if cookie in mvCookie:
            (mvFrom, _, _) = mvCookie[cookie]
            del mvCookie[cookie]
            if isDir:
                activity.onMovedDirectory(mvFrom, mvTo)
            else:
                activity.onMovedFile(mvFrom, mvTo)
        else:
            mvCookie[cookie] = (path, action, eventCount+5)
    else:
        checkMoveEvents()
        if isDir:
            if action == 'IN_CREATE':
                activity.onNewDirectory(path)
            elif action == 'IN_DELETE':
                activity.onDeletedDirectory(path)
            elif action == 'IN_ATTRIB':
                activity.onDirMetadataChanged(path)
            elif action == 'IN_IGNORED' or action == 'IN_DELETE_SELF' or action == 'IN_MOVE_SELF':
                pass
            else:
                print("Suppressing ISDIR %s %s" % (action, path))
        else:     
            #print("NEW_FILE "+path)
            """
            { 'Records': [{'file_path': path, 'timestamp': '', 'eventSource: 'dcache'}]}
            """
            if action == 'IN_CLOSE_WRITE':
                f = open(workfolder+"/dcache"+str(uuid.uuid4())+".txt", "w")
                f.write(str(msg))
                f.close()
                activity.onNewFile(path)
            elif action == 'IN_DELETE':
                activity.onDeletedFile(path)
            elif action == 'IN_ATTRIB':
                activity.onFileMetadataChanged(path)
            elif action == 'IN_IGNORED' or action == 'IN_DELETE_SELF' or action == 'IN_CREATE':
                pass
            else:
                print("Suppressing %s %s" % (action, path))

mvCookie = {}
watches = {}


def normalise_path(path):
    "Strip off any trailing '/' in any non-root path"
    return path if path == "/" or not path.endswith("/") else path[:-1]


def remove_redundant_paths(paths):
    "Return a list of paths where any subdirectories have been removed"
    non_redundant_paths = []
    for path in paths:
        paths_to_remove = []
        for non_redundant_path in non_redundant_paths:
            if path.startswith(non_redundant_path + "/"):
                print("Skipping redundant path: %s" % path)
                break
            elif non_redundant_path.startswith(path + "/"):
                print("Skipping redundant path: %s" % non_redundant_path)
                paths_to_remove.append(non_redundant_path)
        else:
            non_redundant_paths.append(path)
        for remove_path in paths_to_remove:
            non_redundant_paths.remove(remove_path)
    return non_redundant_paths


def create_channel_and_watches(s):
    "Create a channel and include all watches"
    channel = request_channel(s)

    paths = map(normalise_path, args["paths"])
    if isRecursive:
        paths = remove_redundant_paths(paths)
        for path in paths:
            recursive_watch(channel, path)
    else:
        for path in paths:
            single_watch(channel, path)

    if not watches:
        exit("No watches established, exiting...")

    return channel


def restore_channel_and_watches(path):
    try:
        with open(path) as f:
            is_first = True
            for line in f.readlines():
                if is_first:
                    (channel,last_id) = line.split()
                    print("Restoring channel")
                    is_first = False
                else:
                    (watch,encoded_path) = line.split()
                    path = requests.utils.unquote(encoded_path)
                    print("Restoring watch %s" % path)
                    watches[watch] = path

    except FileNotFoundError:
        channel = create_channel_and_watches(s)
        last_id = None

    return (channel,last_id)

s = configure_session(args)

if state_path:
    (channel,last_id) = restore_channel_and_watches(state_path)
else:
    channel = create_channel_and_watches(s)
    last_id = None

try:
    while True:
        try:
            if last_id:
                messages = SSEClient(channel, session=s, last_id=last_id)
            else:
                messages = SSEClient(channel, session=s)

            for msg in messages:
                eventCount = eventCount + 1
                eventType = msg.event
                data = json.loads(msg.data)
                if eventType == "SYSTEM":
                    type = data["type"]
                    if type == "EVENT_LOSS":
                        activity.onEventLoss()
                    elif type != "NEW_SUBSCRIPTION" and type != "SUBSCRIPTION_CLOSED":
                        print("SYSTEM: %s" % msg.data)
                else:
                    sub = data["subscription"]
                    event = data["event"]
                    print(data)
                    if eventType == 'inotify':
                        inotify(eventType, sub, event,msg)
                    else:
                        print("Unknown event: %s", type)
                        print("    Subscription: %s", sub)
                        print("    Data: %s", event)

                if msg.id:
                    
                    last_id = msg.id
                    if state_path != None and last_id != None:
                        #print("Saving state for resumption")
                        with open(state_path, 'w') as f:
                            f.write("{} {}\n".format(channel, last_id))
                            for watch,path in watches.items():
                                f.write("{} {}\n".format(watch, requests.utils.quote(path)))
                    #exit(0)

        except requests.exceptions.HTTPError as e:
            r = e.response
            if r.status_code == 404:
                print("Recovering from unknown channel")
                channel = create_channel_and_watches(s)
                last_id = None
            else:
                print("HTTP error {} {}".format(r.status_code, r.reason))
                break

except KeyboardInterrupt:
    print("Interrupting...")

finally:
    if state_path != None and last_id != None:
        print("Saving state for resumption")
        with open(state_path, 'w') as f:
            f.write("{} {}\n".format(channel, last_id))
            for watch,path in watches.items():
                f.write("{} {}\n".format(watch, requests.utils.quote(path)))
    else:
        print("Deleting channel")
        s.delete(channel)
        try:
            os.remove(state_path)
        except FileNotFoundError:
            pass
    activity.close()
