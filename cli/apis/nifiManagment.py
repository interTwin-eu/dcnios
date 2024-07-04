# dCNiOs
# Copyright (C) 2023 - GRyCAP - Universitat Politecnica de Valencia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache 2.0 licence as published by
# the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache 2.0 License for more details.
#
# You should have received a copy of the Apache 2.0 License
# along with this program.  If not, see <https://www.apache.org/licenses/>.

import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth
from urllib3 import encode_multipart_formdata
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Nifi:

    def __init__(self, nifi_endPoint, user, password):
        self.nifi_url = nifi_endPoint   # +":"+nifi_Port
        self.basic = HTTPBasicAuth(user, password)

    def callHttp(self, type, link, data, header='application/json'):
        try:
            response = type(self.nifi_url+link,
                            headers={'Content-Type': header},
                            data=data, auth=self.basic, verify=False)
            return response
        except requests.exceptions as e:  # This is the correct syntax
            print(e)

    def startProcess(self, name):
        process_groupid = self.getProcessGroup(name)
        link = "/nifi-api/flow/process-groups/" + process_groupid
        data = '{"id":"' + process_groupid + '","state":"RUNNING"}'
        response = self.callHttp(requests.put, link, data)

    def stopProcess(self, name):
        process_groupid = self.getProcessGroup(name)
        link = "/nifi-api/flow/process-groups/" + process_groupid
        data = '{"id":"' + process_groupid + '","state":"STOPPED"}'
        response = self.callHttp(requests.put, link, data)

    def makeConnection(self, fromName, toName):
        fromGroupid = self.getProcessGroup(fromName)
        toGroupid = self.getProcessGroup(toName)
        response = self.callHttp(requests.get,
                                 "/nifi-api/process-groups/root/connections",
                                 '')
        for connection in response.json()["connections"]:
            if connection["component"]["source"]["groupId"] == fromGroupid \
                    and connection["component"]["destination"]["groupId"] == \
                    toGroupid:
                return connection["id"]
        response = self.callHttp(requests.get, "/nifi-api/process-groups/"
                                 + toGroupid + "/input-ports", '')
        destinationid = response.json()["inputPorts"][0]["id"]

        response = self.callHttp(requests.get, "/nifi-api/process-groups/"
                                 + fromGroupid + "/output-ports", '')
        sourceid = response.json()["outputPorts"][0]["id"]
        link = "/nifi-api/process-groups/root/connections"
        data = '{"revision":{"version": 0},"component": {' \
            + ' "source": { "id": "' \
            + sourceid + '", "groupId": "' + fromGroupid \
            + '", "type": "OUTPUT_PORT" }, "destination": {  "id": "' \
            + destinationid + '", "groupId": "' + toGroupid \
            + '", "type": "INPUT_PORT" } } }'
        response = self.callHttp(requests.post, link, data)
        return response.json()["id"]

    def deleteProcess(self, name):
        groupid = self.getProcessGroup(name)
        if not groupid:
            return None
        process_group = groupid
        response = self.callHttp(requests.get,
                                 "/nifi-api/process-groups/root/connections", '')
        for connection in response.json()["connections"]:
            if connection["component"]["source"]["groupId"] == process_group \
                    or connection["component"]["destination"]["groupId"] == process_group:
                link = "/nifi-api/connections/" + connection["id"] \
                    + "?version=" + str(connection["revision"]["version"])
                response = self.callHttp(requests.delete, link, '')

        response = self.callHttp(requests.get, "/nifi-api/process-groups/"
                                 + process_group, '')
        version = str(response.json()["revision"]["version"])
        response = self.callHttp(requests.delete, "/nifi-api/process-groups/"
                                 + process_group + "?version=" + version, '')

    def getProcessGroup(self, process_groupName):
        response = self.callHttp(requests.get,
                                 "/nifi-api/process-groups"
                                 + "/root/process-groups", '')
        for pg in response.json()["processGroups"]:
            if (pg["component"]["name"] == process_groupName):
                return pg["id"]
        return None

    def create(self, name, filecontent):
        groupid = self.getProcessGroup(name)
        if not groupid:
            fields = {"groupName": name, "positionX": "-150",
                      "positionY": "-150", "clientId": "aaa",
                      "file": ("namefile",
                               json.dumps(filecontent).encode('utf-8'),
                               "application/json"), }
            body, header = encode_multipart_formdata(fields)
            response = self.callHttp(requests.post,
                                     "/nifi-api/process-groups"
                                     + "/root/process-groups/upload",
                                     body,
                                     header)

    def changeVariable(self, name, key, value):
        id = self.getProcessGroup(name)
        response = self.callHttp(requests.get,
                                 "/nifi-api/process-groups/"
                                 + id + "/variable-registry",
                                 '')
        PGRversion = response.json()["processGroupRevision"]["version"]
        data = '{"processGroupRevision": { "version": ' \
            + str(PGRversion) + '}, \
            "variableRegistry": {"variables": [ { "variable": {         \
                    "name": "' + key + '",                      \
                    "value": "' + value + '"                     \
                    } } ], "processGroupId": "' + id + '" }}'
        response = self.callHttp(requests.put, "/nifi-api/process-groups/"
                                 + id + "/variable-registry", data)

    def updateProcessor(self, pg, process, accion):
        id = self.getProcessGroup(pg)
        response = self.callHttp(requests.get,
                                 "/nifi-api/flow/process-groups/" + id, '')
        components = response.json()["processGroupFlow"]["flow"]["processors"]
        found = False
        for comp in components:
            if comp["component"]["name"] == process:
                processid = comp["component"]["id"]
                state = comp["component"]["state"]
                found = True
        if not found:
            return False
        else:
            if state == "RUNNING":
                self.stopProcess(pg)
            response = self.callHttp(requests.get, "/nifi-api/processors/"
                                     + processid, '')
            version = response.json()["revision"]["version"]
            execution = response.json()["component"]["config"]["executionNode"]
            data = '{"component": {"id":"' + str(processid) + '", "name":"' \
                + str(process) + '",\
                "config":{'+accion+' }, "state":"STOPPED"},\
                "revision":{"version":' + str(version) \
                + '}, "disconnectedNodeAcknowledged":false}'
            response = self.callHttp(requests.put, "/nifi-api/processors/"
                                     + processid, data)
            if state == "RUNNING":
                self.startProcess(pg)
        return True

    def changeSchedule(self, pg, process, seconds):
        self.updateProcessor(pg, process, '"schedulingPeriod":"'
                             + str(seconds) + ' sec"')

    def executionNode(self, pg, process, node):
        if node == "PRIMARY" or node == "ALL":
            self.updateProcessor(pg, process, '"executionNode":"'+node+'"')
        else:
            pass

    def nifiVersion(self):
        response = self.callHttp(requests.get,
                                 "/nifi-api/system-diagnostics", '')
        infoversion = response.json()["systemDiagnostics"]["aggregateSnapshot"]
        return infoversion["versionInfo"]["niFiVersion"]

    def enableSSL(self, name):
        groupid = self.getProcessGroup(name)
        response = self.callHttp(requests.get, "/nifi-api/flow/process-groups/"
                                 + groupid + "/controller-services", '')
        for controller in response.json()["controllerServices"]:
            if controller["parentGroupId"] == groupid:
                ssl_context_id = controller["id"]
                version = controller["revision"]["version"]
                data = '{"revision":{"clientId":"' + groupid + '","version":' \
                    + str(version) + '},"disconnectedNodeAcknowledged":' \
                    + 'false,"state":"ENABLED","uiOnly":true}'
                response = self.callHttp(requests.put,
                                         "/nifi-api/controller-services/"
                                         + ssl_context_id+"/run-status", data)

    def disableSSL(self, name):
        groupid = self.getProcessGroup(name)
        response = self.callHttp(requests.get, "/nifi-api/flow/process-groups/"
                                 + groupid + "/controller-services", '')
        for controller in response.json()["controllerServices"]:
            if controller["parentGroupId"] == groupid:
                ssl_context_id = controller["id"]
                version = controller["revision"]["version"]
                data = '{"revision":{"clientId":"' + groupid \
                    + '","version":' + str(version) + '},"' \
                    + 'disconnectedNodeAcknowledged":false,' \
                    + '"state":"DISABLED","uiOnly":true}'
                response = self.callHttp(requests.put,
                                         "/nifi-api/controller-services/"
                                         + ssl_context_id + "/run-status",
                                         data)
                
    def updateComponent(self, type):
        if "components" in type:
            print("Process group: "+type["name"])
            for component in type["components"]:
                print("\t- Process: " + component["name"])
                if "seconds" in component:
                    self.changeSchedule(type["name"], component["name"],
                                        component["seconds"])
                    print("\t  New schedule time: "
                        + str(component["seconds"]) + " seconds")
                if "node" in component:
                    self.executionNode(type["name"],
                                    component["name"], component["node"])
                    print("\t  Now executing in node: " + component["node"])

    def newProcessInfo(self, name):
        print("New Process group: " + str(name))