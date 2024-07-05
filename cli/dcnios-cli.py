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
from apis.auxiliaryFunctions import *
from apis.nifiManagment import *
from apis.aws import *
from sources.dcache import *
from destinations.oscar import *
from sources.kafka import *
from sources.generic import *
import env
import argparse

types = ["dCache", "OSCAR", "S3", "SQS", "generic", "Kafka"]
typesSSL = ["Kafka"]

def doType(type, function):
    if type in data["nifi"]:
        for singularoftype in data["nifi"][type]:
            function(singularoftype["name"])
            print(str(function.__qualname__) + " " + singularoftype["name"])


def makeActionWithAllType(allType, function):
    for type in allType:
        doType(type, function)

def functionAll(function):
    for dic in env.info:
        if dic["id"] in data["nifi"]:
            for information in data["nifi"][dic["id"]]:
                function(information["name"])
                print(str(function.__qualname__) + " " + information["name"])
                if "alterations" in information:
                    for alter in information["alterations"]:
                        function(alteration.nameActionReturn(alter["action"],information["name"]))
                        print(str(function.__qualname__) + " " + alteration.nameActionReturn(alter["action"],information["name"]))

def deleteAll(nifi):
    for dic in env.info:
        if dic["id"] in data["nifi"]:
            for information in data["nifi"][dic["id"]]:
                if auxiliaryFunctions.checkExistSsl_context(information):
                    print("Nifi disable ssl "+ information["name"])
                    nifi.disableSSL(information["name"])
                nifi.deleteProcess(information["name"])
                if "alterations" in information:
                    for alter in information["alterations"]:
                        nifi.deleteProcess(alteration.nameActionReturn(alter["action"],information["name"]))
                print("Delete Process "+ information["name"])

            

def createAll(nifi,dic):
    if dic["id"] in data["nifi"]:
        for information in data["nifi"][dic["id"]]:
            informationcontent=auxiliaryFunctions.prepareforAll(dic["file"],information)
            dic['function'](nifi,information,informationcontent)
            auxiliaryFunctions.postJob(information,nifi)



parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')
parser.add_argument('option')
parser.add_argument('--file','-f')
parser.add_argument('--host')
parser.add_argument('--user', "-u")
parser.add_argument('--password', "-p")
parser.add_argument('--processGroup', "-pg")
parser.add_argument('--component', "-c")
parser.add_argument('--seconds', "-s")
args = parser.parse_args()
if args.option is None and args.f is None:
    print("File parameter not found")
    exit(1)
# Open the file and load the file
elif args.option is not None and args.file is not None:
    with open(args.file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        nifi_endpoint = data["nifi"]["endpoint"]
        nifi_user = data["nifi"]["user"]
        nifi_password = data["nifi"]["password"]
        nifi = Nifi(nifi_endpoint, nifi_user, nifi_password)
        if args.option == "apply":
            for info in env.info:
                createAll(nifi,info)
            if "connection" in data["nifi"]:
                for connection in data["nifi"]["connection"]:
                    for info in env.info:
                        if info["id"] in data["nifi"]:
                            for information in data["nifi"][info["id"]]:
                                if connection["from"] == information["name"]:
                                    if "alterations" in information and information["alterations"] != None:
                                        alterName = alteration.nameActionReturn(information["alterations"][-1]["action"],information["name"])
                                        nifi.makeConnection(alterName, connection["to"])
                                    else:
                                        nifi.makeConnection(connection["from"], connection["to"])
        elif args.option == "delete":
            deleteAll(nifi)
                #makeActionWithAllType(typesSSL, nifi.disableSSL)
                #makeActionWithAllType(types, nifi.deleteProcess)
            # Delete of SQS, not the notification
            if "S3" in data["nifi"]:
                for s3 in data["nifi"]["S3"]:
                    s3["queue_name"] = s3["AWS_S3_BUCKET"] + "_events"
                    deleteSQSQueue(s3)
            if "SQS" in data["nifi"]:
                for sqs in data["nifi"]["SQS"]:
                    deleteSQSQueue(sqs)
        elif args.option == "start":
            functionAll(nifi.startProcess)
                #startAll(nifi,info)
            #makeActionWithAllType(types, nifi.startProcess)
        elif args.option == "stop":
            functionAll(nifi.stopProcess)
                #stoptAll(nifi,info)
            #makeActionWithAllType(types, nifi.stopProcess)
        else:
            print("incorrect command try again")
if args.option == "changeSchedule" or args.option == "cs":
    nifi = Nifi(args.host, args.user, args.password)
    nifi.changeSchedule(args.processGroup, args.component, args.seconds)
    print("Process group: " + str(args.processGroup))
    print("\t- Process: " + str(args.component) + "\n\t  New schedule time: "
          + str(args.seconds) + " seconds")
