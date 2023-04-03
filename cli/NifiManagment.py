#!/usr/bin/env python3
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.auth import HTTPBasicAuth
from urllib3 import encode_multipart_formdata

class Nifi:
    
    def __init__(self,nifi_endPoint,user,password):
        self.nifi_url=nifi_endPoint #+":"+nifi_Port
        self.basic = HTTPBasicAuth(user, password)

    def callHttp(self,type,link, data,header='application/json'):
        try:
            response = type(self.nifi_url+link, headers={'Content-Type': header},
                        data=data, auth=self.basic, verify=False)
            return response
        except requests.exceptions as e:  # This is the correct syntax
            print (e)
    

    def startProcess(self,name):
        process_groupid=self.getProcessGroup(name)
        link="/nifi-api/flow/process-groups/"+process_groupid
        data='{"id":"'+process_groupid+'","state":"RUNNING"}'
        response= self.callHttp(requests.put,link,data )
       
    
    def stopProcess(self,name):
        process_groupid=self.getProcessGroup(name)
        link="/nifi-api/flow/process-groups/"+process_groupid
        data='{"id":"'+process_groupid+'","state":"STOPPED"}'
        response= self.callHttp(requests.put,link,data)

 
    
    def makeConnection(self,fromName,toName):
        fromGroupid=self.getProcessGroup(fromName)
        toGroupid=self.getProcessGroup(toName)
        response= self.callHttp(requests.get,"/nifi-api/process-groups/root/connections",'')
        for connection in response.json()["connections"]:
            if connection["component"]["source"]["groupId"] == fromGroupid and  \
                connection["component"]["destination"]["groupId"] == toGroupid :
                return connection["id"]
        
        response= self.callHttp(requests.get,"/nifi-api/process-groups/"+toGroupid+"/input-ports",'')
        destinationid=response.json()["inputPorts"][0]["id"]

        response= self.callHttp(requests.get,"/nifi-api/process-groups/"+fromGroupid+"/output-ports",'')
        sourceid=response.json()["outputPorts"][0]["id"]

        link="/nifi-api/process-groups/root/connections"
        data='{"revision":{"version": 0},"component": {  \
            "source": { "id": "' + sourceid + '", "groupId": "'+fromGroupid+'", "type": "OUTPUT_PORT" }, \
            "destination": {  "id": "' + destinationid + '", "groupId": "'+toGroupid+'", "type": "INPUT_PORT" } } }'
        response= self.callHttp(requests.post,link,data)
        return response.json()["id"]

    
    def deleteProcess(self,name):
        groupid=self.getProcessGroup(name)
        if not groupid:
            return None
        process_group=groupid
        response= self.callHttp(requests.get,"/nifi-api/process-groups/root/connections",'')

        for connection in response.json()["connections"]:
            if connection["component"]["source"]["groupId"] == process_group or connection["component"]["destination"]["groupId"] == process_group :
                link="/nifi-api/connections/" + connection["id"] + "?version="+str(connection["revision"]["version"])
                response= self.callHttp(requests.delete,link,'')

        response= self.callHttp(requests.get,"/nifi-api/process-groups/"+process_group,'')
        version=str(response.json()["revision"]["version"])
        response= self.callHttp(requests.delete,"/nifi-api/process-groups/" + process_group + "?version="+version,'')

    def getProcessGroup(self, process_groupName):
        response= self.callHttp(requests.get,"/nifi-api/process-groups/root/process-groups",'')
        for pg in response.json()["processGroups"]:
            if(pg["component"]["name"] == process_groupName):
                return pg["id"]
        return None


    def create(self,name,file):
        groupid=self.getProcessGroup(name)
        if not groupid :
            fields = {"groupName": name, "positionX": "-150","positionY": "-150","clientId" : "aaa",
                      "file": (file, open(file).read(), "application/json"),}
            body, header = encode_multipart_formdata(fields)
            response= self.callHttp(requests.post,"/nifi-api/process-groups/root/process-groups/upload",body,header)

    def changeVariable(self,name,key,value):
        id=self.getProcessGroup(name)
        response= self.callHttp(requests.get,"/nifi-api/process-groups/"+id+"/variable-registry",'')
        PGRversion=response.json()["processGroupRevision"]["version"]
        data='{"processGroupRevision": { "version": '+str(PGRversion)+'}, \
            "variableRegistry": {"variables": [ { "variable": {         \
                    "name": "' + key + '",                      \
                    "value": "'+ value + '"                     \
                    } } ], "processGroupId": "' + id + '" }}'
        response= self.callHttp(requests.put,"/nifi-api/process-groups/"+id+"/variable-registry",data)


    def updateProcessor(self, pg, process, accion):
        id=self.getProcessGroup(pg)
        response= self.callHttp(requests.get,"/nifi-api/flow/process-groups/"+ id,'')
        components=response.json()["processGroupFlow"]["flow"]["processors"]
        found=False
        for comp in components:
            if comp["component"]["name"] == process:
                processid=comp["component"]["id"]
                state=comp["component"]["state"]
                found=True
        if found == False:
            return False
        else:
            if state == "RUNNING":
                self.stopProcess(pg)
            response= self.callHttp(requests.get,"/nifi-api/processors/"+processid,'')
            #print(json.dumps(response.json()["component"]["config"], indent=4))
            version=response.json()["revision"]["version"]
            execution=response.json()["component"]["config"]["executionNode"]
            data='{"component": {"id":"'+str(processid)+'", "name":"'+str(process)+'",                  \
                "config":{'+accion+' }, "state":"STOPPED"}, \
                "revision":{"version":'+str(version)+'}, "disconnectedNodeAcknowledged":false}'     
            response= self.callHttp(requests.put,"/nifi-api/processors/"+ processid,data)
            if state == "RUNNING":
                self.startProcess(pg)
        return True
    
    def changeSchedule(self, pg, process, seconds):
        self.updateProcessor(pg, process, '"schedulingPeriod":"'+str(seconds)+' sec"')

    def executionNode(self, pg, process, node):
        if node == "PRIMARY" or node == "ALL":
            self.updateProcessor(pg, process, '"executionNode":"'+node+'"')
        else:
            pass

    def nifiVersion(self):
        response= self.callHttp(requests.get,"/nifi-api/system-diagnostics",'')
        return response.json()["systemDiagnostics"]["aggregateSnapshot"]["versionInfo"]["niFiVersion"]