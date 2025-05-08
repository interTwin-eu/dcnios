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

# !/usr/bin/env python3

import json
import os
from alterations import alteration
import env


def addSensitiveVariable(file, processorName, key, value):
    for processor in file["flowContents"]["processors"]:
        if processor[env.NAME_TAG] == processorName:
            processor["properties"][key] = value
            return file


def prepareforAll(fileName, info):
    with open(fileName) as f:
        filecontent = json.load(f)
    filecontent["snapshotMetadata"] = {}
    filecontent["snapshotMetadata"]["bucketIdentifier"] = ""
    filecontent["snapshotMetadata"]["flowIdentifier"] = ""
    filecontent["snapshotMetadata"]["version"] = -1
    if checkExistSsl_context(info):
        filecontent = ssl_context(filecontent,info[env.SSL_CONTEXT_TAG])
    return filecontent

def postJob(info,nifi):
    if checkExistSsl_context(info):
        print("Nifi enable ssl "+ info[env.NAME_TAG])
        nifi.enableSSL(info[env.NAME_TAG])
    nifi.newProcessInfo(info[env.NAME_TAG])
    nifi.updateComponent(info)
    if env.ALTERATION_ALTERATIONS_TAG in info:
        alteration.createAlteration(nifi,info)



def checkExistSsl_context(info):
    if env.SSL_CONTEXT_TAG in info:
        return True
    else:
        return False

def ssl_context(filecontent, variables):
    if filecontent["flowContents"]["controllerServices"]==[]:
        introduceSSL(filecontent)
    else:
        pass
    for var in variables:
        change = filecontent["flowContents"]["controllerServices"][0]
        change["properties"][var.replace("_", " ")] = variables[var]
    return filecontent


def introduceSSL(filecontent):
    with open("apis/sslExample") as f:
        sslcontent = json.load(f)
    filecontent["flowContents"]["controllerServices"] = sslcontent
