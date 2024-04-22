# dCNiOs 
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
from oscar_python.client import Client
from sources.auxiliaryFunctions import *
from sources.NifiManagement import *
from sources.aws import * 
import boto3
import os
import argparse

folder="template/"
dcachefile=folder+"dcache.json"
oscarfile=folder+"InvokeOSCAR.json"
sqsfile=folder+"SQS_recive.json"
kafkafile=folder+"Kafka.json"
types=["dCache","OSCAR","S3","SQS","generic","Kafka"]
typesSSL=["Kafka"]

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
        for singularoftype in data["nifi"][type]:
            function(singularoftype["name"])
            print(str(function.__qualname__)+ " " + singularoftype["name"])

def makeActionWithAllType(allType,function):
    for type in allType:
        doType(type,function)

def newProcessInfo(name):
    print("New Process group: "+ str(name))



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
            if "dCache" in data["nifi"]:
                for dcache in data["nifi"]["dCache"]:
                    dcachecontent=prepareforAll(dcachefile)
                    nifi.create(dcache["name"], dcachecontent )
                    command="simple-client.py --state /state/"+dcache["statefile"]+" --endpoint "+ \
                        dcache["endpoint"]+" --user "+dcache["user"]+" --password "+ \
                        dcache["password"]+" "+ dcache["folder"]
                    nifi.changeVariable(dcache["name"],"command",command)
                    newProcessInfo(dcache["name"])
                    updateComponent(dcache)

            if "OSCAR" in data["nifi"]:
                for oscar in data["nifi"]["OSCAR"]:
                    oscarcontent=prepareforAll(oscarfile)
                    nifi.create(oscar["name"],oscarcontent)
                    nifi.changeVariable(oscar["name"],"endpoint", oscar["endpoint"])
                    nifi.changeVariable(oscar["name"],"service", oscar["service"])
                    if "user" in oscar and "password" in oscar:
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
                    genericcontent=prepareforAll(generic["file"])
                    nifi.create(generic["name"],genericcontent)
                    for variable in generic["variables"]:
                        nifi.changeVariable(generic["name"],variable,generic["variables"][variable])
                    newProcessInfo(generic["name"])
                    updateComponent(generic)
            if "SQS" in data["nifi"]:
                for sqs in data["nifi"]["SQS"]:
                    #Get credentials of AWS
                    getAWSCredentials(sqs)
                    #Create SQS
                    sqsDetails=createSQS(sqs)
                    #Prepare config
                    sqscontent=prepareforAll(sqsfile)
                    sqscontent=sqsPreparefile(sqscontent,sqs)
                    #Create object
                    nifi.create(sqs["name"],sqscontent)
                    nifi.changeVariable(sqs["name"],'queueurl',sqsDetails['QueueUrl'])
                    newProcessInfo(sqs["name"])
                    updateComponent(sqs)          
            if "S3" in data["nifi"]:
                for s3 in data["nifi"]["S3"]:
                    #Get credentials of AWS
                    getAWSCredentials(s3)
                    #Create SQS
                    s3["queue_name"]= s3["AWS_S3_BUCKET"]+"_events"
                    sqsDetails=createSQS(s3)
                    #Create Notification from S3 event to SQS
                    s3NotificationSQS(s3)
                    #Prepare config
                    sqscontent=prepareforAll(sqsfile)
                    s3content=sqsPreparefile(sqscontent,s3)
                    #Create object
                    nifi.create(s3["name"],sqscontent)
                    nifi.changeVariable(s3["name"],'queueurl',sqsDetails['QueueUrl'])
                    newProcessInfo(s3["name"])
                    updateComponent(s3)
            if "Kafka" in data["nifi"]:
                for kafka in data["nifi"]["Kafka"]:
                    #Prepare config
                    kafkacontent=prepareforAll(kafkafile)
                    kafkacontent=kafkaPreparefile(kafkacontent,kafka)
                    #Set ssl context configuration
                    kafka["ssl_context"]["SSL_Protocol"]="TLS"
                    kafka["ssl_context"]["Truststore_Type"]="PKCS12"
                    kafka["ssl_context"]["Truststore_Filename"]="/opt/nifi/nifi-current/data/"+kafka["ssl_context"]["Truststore_Filename"]
                    kafkacontent=ssl_context(kafkacontent,kafka["ssl_context"])
                    #Create object
                    nifi.create(kafka["name"],kafkacontent)
                    nifi.changeVariable(kafka["name"],"group_id", kafka["group_id"])
                    nifi.changeVariable(kafka["name"],"bootstrap_servers", kafka["bootstrap_servers"])
                    nifi.changeVariable(kafka["name"],"topic", kafka["topic"])
                    #enable SSL
                    nifi.enableSSL(kafka["name"])
                    newProcessInfo(kafka["name"])
                    updateComponent(kafka)                    
            if "connection" in data["nifi"]:
                for connection in data["nifi"]["connection"]:
                    nifi.makeConnection(connection["from"],connection["to"])
        elif args.option == "delete":
                makeActionWithAllType(typesSSL,nifi.disableSSL)
                makeActionWithAllType(types,nifi.deleteProcess)
                #Delete of SQS, not the notification
                if "S3" in data["nifi"]:
                    for s3 in data["nifi"]["S3"]:
                        s3["queue_name"]= s3["AWS_S3_BUCKET"]+"_events"
                        deleteSQS(s3)
                if "SQS" in data["nifi"]:
                    for sqs in data["nifi"]["S3"]:
                        deleteSQS(sqs)
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