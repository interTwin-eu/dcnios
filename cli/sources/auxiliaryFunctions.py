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

#!/usr/bin/env python3

import json
import os

def addSensibleVariable(file,processorName,key,value):
    for processor in file["flowContents"]["processors"]:
        if processor["name"] == processorName:
            processor["properties"][key]=value
            return file


def prepareforAll(fileName):
    with open(fileName) as f:
            filecontent = json.load(f)
    filecontent["snapshotMetadata"]={}
    filecontent["snapshotMetadata"]["bucketIdentifier"]=""
    filecontent["snapshotMetadata"]["flowIdentifier"]=""
    filecontent["snapshotMetadata"]["version"]=-1
    return filecontent

 
def kafkaPreparefile(filecontent,kafka):
    if "security_protocol" not in kafka:
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","security.protocol","SASL_SSL")
    else:
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","security.protocol",kafka["security_protocol"])
    if "" not in kafka:
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","sasl.mechanism","PLAIN")
    else:
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","sasl.mechanism",kafka["sasl_mechanism"])
    filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","sasl.username",kafka["sasl_username"])
    filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","sasl.password",kafka["sasl_password"])
    if "separate_by_key" in kafka and kafka["separate_by_key"] == "true" :
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","separate-by-key","true")
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","message-demarcator",kafka["message_demarcator"])
    else:  
        filecontent=addSensibleVariable(filecontent,"ConsumeKafka_2_6","separate-by-key","false")
    return filecontent 

def ssl_context(filecontent, variables):
     for var in variables:
         filecontent["flowContents"]["controllerServices"][0]["properties"][var.replace("_", " ")]=variables[var]
     return filecontent
