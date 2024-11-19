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
from apis import nifiManagment
import env

def createKafka(nifiConfiguration,kafkaInfo,kafkacontent):
    # Prepare config
    kafkacontent = kafkaPreparefile(kafkacontent, kafkaInfo)
    # Set ssl context configuration
    kafkaInfo[env.SSL_CONTEXT_TAG]["SSL_Protocol"] = "TLS"
    kafkaInfo[env.SSL_CONTEXT_TAG]["Truststore_Type"] = "PKCS12"
    kafkaInfo[env.SSL_CONTEXT_TAG][env.SSL_TRUSTORE_FILENAME_TAG] = "/opt/nifi" \
        + "/nifi-current/data/" \
        + kafkaInfo[env.SSL_CONTEXT_TAG][env.SSL_TRUSTORE_FILENAME_TAG]
    kafkacontent = auxiliaryFunctions.ssl_context(kafkacontent,
                                                  kafkaInfo[env.SSL_CONTEXT_TAG])
    # Create object
    nifiConfiguration.create(kafkaInfo[env.NAME_TAG], kafkacontent)
    nifiConfiguration.changeVariable(kafkaInfo[env.NAME_TAG], "group_id",
                        kafkaInfo[env.KAFKA_GROUP_ID_TAG])
    nifiConfiguration.changeVariable(kafkaInfo[env.NAME_TAG], "bootstrap_servers",
                        kafkaInfo[env.KAFKA_BOOTSTRAP_SERVERS_TAG])
    nifiConfiguration.changeVariable(kafkaInfo[env.NAME_TAG], "topic",
                        kafkaInfo[env.KAFKA_TOPIC_TAG])






def kafkaPreparefile(filecontent, kafka):
    if "security_protocol" not in kafka:
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "security.protocol", "SASL_SSL")
    else:
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "security.protocol",
                                          kafka[env.KAFKA_SECURITY_PROTOCOL_TAG])
    if "" not in kafka:
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "sasl.mechanism", "PLAIN")
    else:
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "sasl.mechanism",
                                          kafka[env.KAFKA_SASL_MECHANISM_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                      "sasl.username",
                                      kafka[env.KAFKA_SASL_USERNAME_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                      "sasl.password",
                                      kafka[env.KAFKA_SASL_PASSWORD_TAG])
    if env.KAFKA_SEPARATE_BY_KEY_TAG in kafka and kafka[env.KAFKA_SEPARATE_BY_KEY_TAG] == "true":
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "separate-by-key", "true")
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "message-demarcator",
                                          kafka[env.KAFKA_MESSAGE_DEMARCATOR_TAG])
    else:
        filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, "ConsumeKafka_2_6",
                                          "separate-by-key", "false")
    return filecontent
