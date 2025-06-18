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


def functionAll(function):
    for dic in env.info:
        if dic["id"] in data[env.NIFI_TAG][dic["type"]]:
            for information in data[env.NIFI_TAG][dic["type"]][dic["id"]]:
                function(information[env.NAME_TAG])
                print(str(function.__qualname__) + " " + information[env.NAME_TAG])
                if env.ALTERATION_ALTERATIONS_TAG in information:
                    for alter in information[env.ALTERATION_ALTERATIONS_TAG]:
                        function(alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))
                        print(str(function.__qualname__) + " " + alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))
    if env.GENERIC_TAG in data[env.NIFI_TAG]:
        for information in data[env.NIFI_TAG][env.GENERIC_TAG]:
                function(information[env.NAME_TAG])
                print(str(function.__qualname__) + " " + information[env.NAME_TAG])
                if env.ALTERATION_ALTERATIONS_TAG in information:
                    for alter in information[env.ALTERATION_ALTERATIONS_TAG]:
                        function(alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))
                        print(str(function.__qualname__) + " " + alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))


def deleteAll(nifi):
    for dic in env.info:
        if dic["id"] in data[env.NIFI_TAG][dic["type"]]:
            for information in data[env.NIFI_TAG][dic["type"]][dic["id"]]:
                if auxiliaryFunctions.checkExistSsl_context(information):
                    print("Nifi disable ssl " + information[env.NAME_TAG])
                    nifi.disableSSL(information[env.NAME_TAG])
                nifi.deleteProcess(information[env.NAME_TAG])
                if env.ALTERATION_ALTERATIONS_TAG in information:
                    for alter in information[env.ALTERATION_ALTERATIONS_TAG]:
                        nifi.deleteProcess(alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))
                print("Delete Process " + information[env.NAME_TAG])
    if env.GENERIC_TAG in data[env.NIFI_TAG]:
        for information in data[env.NIFI_TAG][env.GENERIC_TAG]:
            if auxiliaryFunctions.checkExistSsl_context(information):
                print("Nifi disable ssl " + information[env.NAME_TAG])
                nifi.disableSSL(information[env.NAME_TAG])
            nifi.deleteProcess(information[env.NAME_TAG])
            if env.ALTERATION_ALTERATIONS_TAG in information:
                for alter in information[env.ALTERATION_ALTERATIONS_TAG]:
                    nifi.deleteProcess(alteration.nameActionReturn(alter[env.ALTERATION_ACTION_TAG], information[env.NAME_TAG]))
            print("Delete Process " + information[env.NAME_TAG])


def createAll(nifi):
    for dic in env.info:
        if dic["id"] in data[env.NIFI_TAG][dic["type"]]:
            for information in data[env.NIFI_TAG][dic["type"]][dic["id"]]:
                informationcontent = auxiliaryFunctions.prepareforAll(dic["file"], information)
                dic['function'](nifi, information, informationcontent)
                auxiliaryFunctions.postJob(information, nifi)
    if env.GENERIC_TAG in data[env.NIFI_TAG]:
        for information in data[env.NIFI_TAG][env.GENERIC_TAG]:
            informationcontent = auxiliaryFunctions.prepareforAll(information[env.GENERIC_FILE_TAG], information)
            createGeneric(nifi, information, informationcontent)
            auxiliaryFunctions.postJob(information, nifi)


parser = argparse.ArgumentParser(
    prog='dcnios-cli.py',
    description='DCNiOS, Data Connector through Apache NiFi for OSCAR, \
facilitates the creation of event-driven processes connecting a Storage \
System like dCache or Amazon S3 to a scalable OSCAR cluster by employing \
predefined dataflows that are processed by Apache NiFi.',
    epilog='Text at the bottom of help',
    usage="%(prog)s [-h] \n \
                    | [apply | start | stop | delete ] --file FILE \n \
                    | changeSchedule --host HOST --user USER --password PASSWORD \n \
                      --processGroup PROCESSGROUP --component COMPONENT --seconds SECONDS")
parser.add_argument('action',
                    choices=["apply", "start", "stop", "delete", "changeSchedule"],
                    help='',
                    )
parser.add_argument('--file', '-f', help='Use a file to [apply | start | stop | delete ] a workflow')
parser.add_argument('--host', help='Define the host only for the action of changeSchedule')
parser.add_argument('--user', "-u",  help='Define the user only for the action of changeSchedule')
parser.add_argument('--password', "-p",  help='Define the password only for the action of changeSchedule')
parser.add_argument('--processGroup', "-pg",  help='Define the processGroup only for the action of changeSchedule')
parser.add_argument('--component', "-c",  help='Define the component only for the action of changeSchedule')
parser.add_argument('--seconds', "-s",  help='Define the seconds only for the action of changeSchedule')
args = parser.parse_args()


if args.action is None and args.f is None:
    print("File parameter not found")
    exit(1)
# Open the file and load the file
elif args.action is not None and args.file is not None:
    with open(args.file) as f:
        data = yaml.load(f, Loader=SafeLoader)
        nifi_endpoint = data[env.NIFI_TAG]["endpoint"]
        nifi_user = data[env.NIFI_TAG]["user"]
        nifi_password = data[env.NIFI_TAG]["password"]
        nifi = Nifi(nifi_endpoint, nifi_user, nifi_password)
        if args.action == "apply":
            createAll(nifi)
            if env.CONNECTION_TAG in data[env.NIFI_TAG]:
                for connection in data[env.NIFI_TAG][env.CONNECTION_TAG]:
                    for info in env.info:
                        if info["id"] in data[env.NIFI_TAG][env.SOURCE_TAG]:
                            for information in data[env.NIFI_TAG][env.SOURCE_TAG][info["id"]]:
                                if connection[env.CONNECTION_FROM_TAG] == information[env.NAME_TAG]:
                                    if env.ALTERATION_ALTERATIONS_TAG in information and information[env.ALTERATION_ALTERATIONS_TAG] is not None:
                                        alterName = alteration.nameActionReturn(information[env.ALTERATION_ALTERATIONS_TAG][-1][env.ALTERATION_ACTION_TAG], information[env.NAME_TAG])
                                        nifi.makeConnection(alterName, connection[env.CONNECTION_TO_TAG])
                                    else:
                                        nifi.makeConnection(connection[env.CONNECTION_FROM_TAG], connection[env.CONNECTION_TO_TAG])
        elif args.action == "delete":
            deleteAll(nifi)
            # Delete of SQS, not the notification
            if env.S3_TAG in data[env.NIFI_TAG]:
                for s3 in data[env.NIFI_TAG][env.S3_TAG]:
                    s3[env.QUEUE_NAME_TAG] = s3[env.AWS_S3_BUCKET_TAG] + "_events"
                    deleteSQSQueue(s3)
            if env.SQS_TAG in data[env.NIFI_TAG]:
                for sqs in data[env.NIFI_TAG][env.SQS_TAG]:
                    deleteSQSQueue(sqs)
        elif args.action == "start":
            functionAll(nifi.startProcess)
        elif args.action == "stop":
            functionAll(nifi.stopProcess)
        else:
            print("incorrect command try again")
if args.action == "changeSchedule" or args.action == "cs":
    nifi = Nifi(args.host, args.user, args.password)
    nifi.changeSchedule(args.processGroup, args.component, args.seconds)
    print("Process group: " + str(args.processGroup))
    print("\t- Process: " + str(args.component) + "\n\t  New schedule time: "
          + str(args.seconds) + " seconds")
