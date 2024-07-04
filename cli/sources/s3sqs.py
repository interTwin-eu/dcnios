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
import boto3
from apis import auxiliaryFunctions
from apis import nifiManagment
from apis import aws



def createGetS3(nifiConfiguration,s3Info,s3content):
    s3Info["queue_name"] = s3Info["AWS_S3_BUCKET"] + "_events"
    createGetSQS(nifiConfiguration,s3Info,s3content)
    aws.s3NotificationSQS(s3Info)


def createGetSQS(nifiConfiguration,sqsInfo,sqscontent):
    # Get credentials of AWS
    aws.getAWSCredentials(sqsInfo)
    # Create SQS
    sqsDetails = aws.createSQSQueue(sqsInfo)
    # Prepare config
    sqscontent = aws.awsCredentialPreparefile(sqscontent, sqsInfo,"GetSQS")
    # Create object
    nifiConfiguration.create(sqsInfo["name"], sqscontent)
    nifiConfiguration.changeVariable(sqsInfo["name"], 'queueurl',
                        sqsDetails['QueueUrl'])