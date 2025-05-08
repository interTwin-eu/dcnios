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


from sources.dcache import createDcache
from sources.s3sqs import createGetS3,createGetSQS
from sources.kafka import createKafka
from sources.generic import createGeneric
from destinations.oscar import createOSCAR
from destinations.s3aws import createPutS3

folderSource = "template/sources/"

kafkafile = folderSource+"Kafka.json"
dcachefile = folderSource+"dcache.json"
sqsfile = folderSource+"SQS_recive.json"

folderDestination = "template/destinations/"
putS3file= folderDestination+ "PutS3.json"
oscarfile = folderDestination+"InvokeOSCAR.json"

NIFI_TAG="nifi"
NAME_TAG="name"
VARIABLE_TAG="variables"

ALTERATION_ALTERATIONS_TAG="alterations"
ALTERATION_ACTION_TAG="action"
ALTERATION_MERGE_TAG="Merge"
ALTERATION_ENCODE_TAG="Encode"
ALTERATION_DECODE_TAG="Decode"
ALTERATION_ENCODING_TAG="Encoding"
ALTERATION_MAX_MESSAGES_TAG="maxMessages"
ALTERATION_WINDOW_SECONDS_TAG="windowSeconds"


SOURCE_TAG="Source"
KAFKA_TAG="Kafka"
KAFKA_BOOTSTRAP_SERVERS_TAG="bootstrap_servers"
KAFKA_TOPIC_TAG="topic"
KAFKA_GROUP_ID_TAG="group_id"
KAFKA_SASL_USERNAME_TAG="sasl_username"
KAFKA_SASL_PASSWORD_TAG="sasl_password"

KAFKA_SASL_MECHANISM_TAG="sasl_mechanism"
KAFKA_SECURITY_PROTOCOL_TAG="security_protocol"
KAFKA_SEPARATE_BY_KEY_TAG="separate_by_key"
KAFKA_MESSAGE_DEMARCATOR_TAG="message_demarcator"

SSL_CONTEXT_TAG="ssl_context"
SSL_TRUSTORE_FILENAME_TAG="Truststore_Filename"
SSL_TRUSTORE_PASSWORD_TAG="Truststore_Password"


DCACHE_TAG="dCache"
DCACHE_ENDPOINT_TAG="endpoint"
DCACHE_USER_TAG="user"
DCACHE_PASSWORD_TAG="password"
DCACHE_FOLDER_TAG="folder"
DCACHE_STATEFILE_TAG="statefile"


SQS_TAG="SQS"
S3_TAG="S3"
AWS_ACCESS_KEY_ID_TAG="AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_TAG="AWS_SECRET_ACCESS_KEY"
AWS_DEFAULT_REGION_TAG="AWS_DEFAULT_REGION"
AWS_S3_BUCKET_TAG="AWS_S3_BUCKET"
QUEUE_NAME_TAG="queue_name"

DESTINATION_TAG="Destination"
OSCAR_TAG="OSCAR"
OSCAR_ENDPOINT_TAG="endpoint"
OSCAR_SERVICE_TAG="service"
OSCAR_TOKEN_TAG="token"
OSCAR_USER_TAG="user"
OSCAR_PASSWORD_TAG="password"


GENERIC_TAG="generic"
GENERIC_FILE_TAG="file"

CONNECTION_TAG="connection"
CONNECTION_TO_TAG="to"
CONNECTION_FROM_TAG="from"

info=[
    {
    'id': DCACHE_TAG,
    'file': dcachefile,
    'function': createDcache,
    'type': SOURCE_TAG,
    },
    {
    'id': OSCAR_TAG,
    'file': oscarfile,
    'function': createOSCAR,
    'type': DESTINATION_TAG,
    },
    {
    'id': 'GetS3',
    'file': sqsfile,
    'function': createGetS3,
    'type': SOURCE_TAG,
    },
        {
    'id': 'PutS3',
    'file': putS3file,
    'function': createPutS3,
    'type': DESTINATION_TAG,
    },
    {
    'id': 'GetSQS',
    'file': sqsfile,
    'function': createGetSQS,
    'type': SOURCE_TAG,
    },
        {
    'id': 'Kafka',
    'file': kafkafile,
    'function': createKafka,
    'type': SOURCE_TAG,

    },
]






