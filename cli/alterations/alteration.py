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

from apis import nifiManagment
from apis import auxiliaryFunctions


def createMerge(nifiConfiguration,information, name):
    nameCompose= nameActionReturn(information["action"],name)
    merge=auxiliaryFunctions.prepareforAll("./template/alterations/Merge.json",information)
    merge = auxiliaryFunctions.addSensitiveVariable(merge, "MergeContent", "Maximum Number of Entries", information["maxMessages"])
    nifiConfiguration.create(nameCompose, merge)
    nifiConfiguration.changeSchedule(nameCompose, "MergeContent", information["windowSeconds"])


def createDecode(nifiConfiguration,information,name):
    nameCompose= nameActionReturn(information["action"],name)
    merge=auxiliaryFunctions.prepareforAll("./template/alterations/Encode_Decode.json",information)
    merge = auxiliaryFunctions.addSensitiveVariable(merge, "EncodeContent", "Mode", "Decode")
    if "Encoding" in information:
        merge = auxiliaryFunctions.addSensitiveVariable(merge, "EncodeContent", "Encoding", information["Encoding"])
    nifiConfiguration.create(nameCompose, merge)

def createEncode(nifiConfiguration,information,name):
    nameCompose= nameActionReturn(information["action"],name)
    merge=auxiliaryFunctions.prepareforAll("./template/alterations/Encode_Decode.json",information)
    if "Encoding" in information:
        merge = auxiliaryFunctions.addSensitiveVariable(merge, "EncodeContent", "Encoding", information["Encoding"])
    nifiConfiguration.create(nameCompose, merge)



def createAlteration(nifiConfiguration,allInformation):
    name=allInformation["name"]
    for alter in allInformation["alterations"]:
        if alter["action"]=="Merge":
            createMerge(nifiConfiguration,alter,name)
        elif alter["action"]=="Encode":
            createEncode(nifiConfiguration,alter,name)
        elif alter["action"]=="Decode":
            createDecode(nifiConfiguration,alter,name)
    connectAlteration(nifiConfiguration,allInformation)


def connectAlteration(nifiConfiguration,allInformation):
    name=allInformation["name"]
    for index,step in enumerate(allInformation["alterations"]):
        if index == 0:
            nifiConfiguration.makeConnection(name,nameActionReturn(step["action"],name))
        else:
            nifiConfiguration.makeConnection(nameActionReturn(allInformation["alterations"][index-1]["action"],name),nameActionReturn(step["action"],name))

def nameActionReturn(nameAction,nameSource):
    return nameAction+ " of "+ nameSource