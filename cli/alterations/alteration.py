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
import env


def createMerge(nifiConfiguration, information, name):
    if env.ALTERATION_ACTION_TAG not in information:
        raise ValueError(f"Missing required key: {env.ALTERATION_ACTION_TAG} in {information}")
    nameCompose = nameActionReturn(information[env.ALTERATION_ACTION_TAG], name)
    merge_config = auxiliaryFunctions.prepareforAll("./template/alterations/Merge.json", information)
    merge_config = auxiliaryFunctions.addSensitiveVariable(merge_config, "MergeContent", "Maximum Number of Entries", information[env.ALTERATION_MAX_MESSAGES_TAG])
    nifiConfiguration.create(nameCompose, merge_config)
    nifiConfiguration.changeSchedule(nameCompose, "MergeContent", information[env.ALTERATION_WINDOW_SECONDS_TAG])


def createDecode(nifiConfiguration, information, name):
    if env.ALTERATION_ACTION_TAG not in information:
        raise ValueError(f"Missing required key: {env.ALTERATION_ACTION_TAG} in {information}")
    nameCompose = nameActionReturn(information[env.ALTERATION_ACTION_TAG], name)
    decode_config = auxiliaryFunctions.prepareforAll("./template/alterations/Encode_Decode.json", information)
    decode_config = auxiliaryFunctions.addSensitiveVariable(decode_config, "EncodeContent", "Mode", "Decode")
    if env.ALTERATION_ENCODING_TAG in information:
        decode_config = auxiliaryFunctions.addSensitiveVariable(decode_config, "EncodeContent", "Encoding", information[env.ALTERATION_ENCODING_TAG])
    nifiConfiguration.create(nameCompose, decode_config)


def createEncode(nifiConfiguration, information, name):
    if env.ALTERATION_ACTION_TAG not in information:
        raise ValueError(f"Missing required key: {env.ALTERATION_ACTION_TAG} in {information}")
    nameCompose = nameActionReturn(information[env.ALTERATION_ACTION_TAG], name)
    encode_config = auxiliaryFunctions.prepareforAll("./template/alterations/Encode_Decode.json", information)
    if env.ALTERATION_ENCODING_TAG in information:
        encode_config = auxiliaryFunctions.addSensitiveVariable(encode_config, "EncodeContent", "Encoding", information[env.ALTERATION_ENCODING_TAG])
    nifiConfiguration.create(nameCompose, encode_config)


def createAlteration(nifiConfiguration, allInformation):
    name = allInformation[env.NAME_TAG]
    for alter in allInformation[env.ALTERATION_ALTERATIONS_TAG]:
        if alter[env.ALTERATION_ACTION_TAG] == env.ALTERATION_MERGE_TAG:
            createMerge(nifiConfiguration, alter, name)
        elif alter[env.ALTERATION_ACTION_TAG] == env.ALTERATION_ENCODE_TAG:
            createEncode(nifiConfiguration, alter, name)
        elif alter[env.ALTERATION_ACTION_TAG] == env.ALTERATION_DECODE_TAG:
            createDecode(nifiConfiguration, alter, name)
    connectAlteration(nifiConfiguration, allInformation)


def connectAlteration(nifiConfiguration, allInformation):
    name = allInformation[env.NAME_TAG]
    for index, step in enumerate(allInformation[env.ALTERATION_ALTERATIONS_TAG]):
        if index == 0:
            nifiConfiguration.makeConnection(name, nameActionReturn(step[env.ALTERATION_ACTION_TAG], name))
        else:
            nifiConfiguration.makeConnection(nameActionReturn(allInformation[env.ALTERATION_ALTERATIONS_TAG][index-1][env.ALTERATION_ACTION_TAG], name),
                                             nameActionReturn(step[env.ALTERATION_ACTION_TAG], name))


def nameActionReturn(nameAction, nameSource):
    return nameAction + " of " + nameSource
