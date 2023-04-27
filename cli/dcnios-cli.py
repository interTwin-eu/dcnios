# Dcnios 
# Copyright (C) 2023 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache 2.0 Licence as published by
# the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache 2.0 License for more details.
#
# You should have received a copy of the Apache 2.0 License
# along with this program.  If not, see <https://www.apache.org/licenses/>.

import yaml
from yaml.loader import SafeLoader
import json
from NifiManagement import *
from oscar_python.client import Client
import sys
import os
import argparse

def updateComponent(type):
    if "components" in type:
        print("Process group: "+type["name"])
        for component in type["components"]:
            print("\t- Process: "+ component["name"])
            if "seconds" in component:
                nifi.changeSchedule(type["name"],component["name"],component["seconds"])
                print("\t  New schedule time: "+ str(component["seconds"]) +" seconds")
            if "node" in component:
                nifi.executionNode(type["name"],component["name"], component["node"])
                print("\t  Now executing in node: "+ component["node"])


def doType(type,function):
    if type in data["nifi"]:
        for type in data["nifi"][type]:
            function(type["name"])
            print(str(function.__qualname__)+ " " + type["name"])

def makeActionWithAllType(allType,function):
    for type in allType:
        doType(type,function)

def newProcessInfo(name):
    print("New Process group: "+ str(name))


folder="template/"
dcachefile=folder+"dcache.json"
oscarfile=folder+"InvokeOSCAR.json"
types=["dcache","oscar","generic"]



parser = argparse.ArgumentParser(prog='ProgramName', description='What the program does', epilog='Text at the bottom of help')
parser.add_argument('option')
parser.add_argument('-f')  
parser.add_argument('--host')
parser.add_argument('--user',"-u")
parser.add_argument('--password',"-p")
parser.add_argument('--processGroup',"-pg")
parser.add_argument('--component',"-c")
parser.add_argument('--seconds',"-s")
args = parser.parse_args()
if args.option  is None and args.f is None:
    print("File parameter not found")
    exit(1)
# Open the file and load the file
elif args.option is not None  and args.f is not None:
    with open(args.f) as f:
        data = yaml.load(f, Loader=SafeLoader)
        nifi_endpoint=data["nifi"]["endpoint"]
        nifi_user=data["nifi"]["user"]
        nifi_password=data["nifi"]["password"]
        nifi=Nifi(nifi_endpoint,nifi_user,nifi_password)
        if args.option == "apply": 
            if "dcache" in data["nifi"]:
                for dcache in data["nifi"]["dcache"]:
                    nifi.create(dcache["name"],dcachefile)
                    command="simple-client.py --state /state/"+dcache["statefile"]+" --endpoint "+ \
                        dcache["endpoint"]+" --user "+dcache["user"]+" --password "+ \
                        dcache["password"]+" "+ dcache["folder"]
                    nifi.changeVariable("dcache","command",command)
                    newProcessInfo(dcache["name"])
                    updateComponent(dcache)

            if "oscar" in data["nifi"]:
                for oscar in data["nifi"]["oscar"]:
                    nifi.create(oscar["name"],oscarfile)
                    nifi.changeVariable(oscar["name"],"endpoint", oscar["endpoint"])
                    nifi.changeVariable(oscar["name"],"service", oscar["service"])
                    if oscar["user"] and oscar["password"]:
                        client = Client("cluster-id",oscar["endpoint"], oscar["user"], oscar["password"], True)
                        service = client.get_service(oscar["service"])
                        token=service.json()["token"]
                        nifi.changeVariable(oscar["name"],"token", token)
                    else:
                        nifi.changeVariable(oscar["name"],"token", oscar["token"])
                    newProcessInfo(oscar["name"])
                    updateComponent(oscar)
            if "generic" in data["nifi"]:
                for generic in data["nifi"]["generic"]:
                    nifi.create(generic["name"],generic["file"])
                    for variable in generic["variables"]:
                        nifi.changeVariable(generic["name"],variable,generic["variables"][variable])
                    newProcessInfo(generic["name"])
                    updateComponent(generic)

            if "connection" in data["nifi"]:
                for connection in data["nifi"]["connection"]:
                    nifi.makeConnection(connection["from"],connection["to"])
        elif args.option == "delete":
                makeActionWithAllType(types,nifi.deleteProcess)
        elif args.option == "start":
                makeActionWithAllType(types,nifi.startProcess)
        elif args.option == "stop":
                makeActionWithAllType(types,nifi.stopProcess)
        else:
            print("incorrect command try again")
if args.option == "changeSchedule" or args.option == "cs":
    nifi=Nifi(args.host,args.user,args.password)
    nifi.changeSchedule(args.processGroup,args.component,args.seconds)
    print("Process group: "+str(args.processGroup))
    print("\t- Process: "+ str(args.component) + "\n\t  New schedule time: "+ str(args.seconds) +" seconds")