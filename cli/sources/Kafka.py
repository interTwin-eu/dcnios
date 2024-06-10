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

from apis import auxiliaryFunctions
from apis import NifiManagment

def createKafka(nifiConfiguration,kafkaInfo,kafkacontent):
    # Prepare config
    kafkacontent = kafkaPreparefile(kafkacontent, kafkaInfo)
    # Set ssl context configuration
    kafkaInfo["ssl_context"]["SSL_Protocol"] = "TLS"
    kafkaInfo["ssl_context"]["Truststore_Type"] = "PKCS12"
    kafkaInfo["ssl_context"]["Truststore_Filename"] = "/opt/nifi" \
        + "/nifi-current/data/" \
        + kafkaInfo["ssl_context"]["Truststore_Filename"]
    kafkacontent = auxiliaryFunctions.ssl_context(kafkacontent,
                                                  kafkaInfo["ssl_context"])
    # Create object
    nifiConfiguration.create(kafkaInfo["name"], kafkacontent)
    nifiConfiguration.changeVariable(kafkaInfo["name"], "group_id",
                        kafkaInfo["group_id"])
    nifiConfiguration.changeVariable(kafkaInfo["name"], "bootstrap_servers",
                        kafkaInfo["bootstrap_servers"])
    nifiConfiguration.changeVariable(kafkaInfo["name"], "topic",
                        kafkaInfo["topic"])






def kafkaPreparefile(filecontent, kafka):
    if "security_protocol" not in kafka:
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "security.protocol", "SASL_SSL")
    else:
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "security.protocol",
                                          kafka["security_protocol"])
    if "" not in kafka:
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "sasl.mechanism", "PLAIN")
    else:
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "sasl.mechanism",
                                          kafka["sasl_mechanism"])
    filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                      "sasl.username",
                                      kafka["sasl_username"])
    filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                      "sasl.password",
                                      kafka["sasl_password"])
    if "separate_by_key" in kafka and kafka["separate_by_key"] == "true":
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "separate-by-key", "true")
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "message-demarcator",
                                          kafka["message_demarcator"])
    else:
        filecontent = auxiliaryFunctions.addSensibleVariable(filecontent, "ConsumeKafka_2_6",
                                          "separate-by-key", "false")
    return filecontent
