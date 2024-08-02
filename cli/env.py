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

info=[
    {
    'id': 'dCache',
    'file': dcachefile,
    'function': createDcache,
    },
    {
    'id': 'OSCAR',
    'file': oscarfile,
    'function': createOSCAR,
    },
    {
    'id': 'GetS3',
    'file': sqsfile,
    'function': createGetS3,
    },
        {
    'id': 'PutS3',
    'file': putS3file,
    'function': createPutS3,
    },
    {
    'id': 'GetSQS',
    'file': sqsfile,
    'function': createGetSQS,

    },
        {
    'id': 'generic',
    'file': oscarfile,
    'function': createGeneric,

    },
        {
    'id': 'Kafka',
    'file': kafkafile,
    'function': createKafka,

    },
]






