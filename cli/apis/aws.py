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
from apis.auxiliaryFunctions import addSensitiveVariable
from apis import auxiliaryFunctions
from apis import nifiManagment

def getAWSCredentials(configuration):
    if "AWS_ACCESS_KEY_ID" in os.environ and os.environ["AWS_ACCESS_KEY_ID"] != "" \
        and "AWS_SECRET_ACCESS_KEY" in os.environ \
            and os.environ["AWS_SECRET_ACCESS_KEY"] != "":
        print("AWS Credentials: Credentials from environment")
        configuration["AWS_ACCESS_KEY_ID"] = os.environ["AWS_ACCESS_KEY_ID"]
        configuration["AWS_SECRET_ACCESS_KEY"] = \
            os.environ["AWS_SECRET_ACCESS_KEY"]
    elif os.path.exists(os.environ["HOME"] + "/.aws/credentials"):
        print("AWS Credentials: Credentials from credentials file")
        session = boto3.Session(profile_name="default")
        credentials = session.get_credentials()
        configuration["AWS_ACCESS_KEY_ID"] = credentials.access_key
        configuration["AWS_SECRET_ACCESS_KEY"] = \
            credentials.secret_key
    elif "AWS_ACCESS_KEY_ID" in configuration \
            and "AWS_SECRET_ACCESS_KEY" in configuration:
        print("AWS Credentials: Credentials from configuration file")


def createSQSQueue(configuration):
    accountID = boto3.client('sts').get_caller_identity().get('Account')
    sqsClient = boto3.client('sqs',
                             region_name=configuration["AWS_DEFAULT_REGION"])
    response = sqsClient.create_queue(QueueName=configuration["queue_name"],
                                      Attributes={
                                          "SqsManagedSseEnabled": "false",
                                          "Policy": '{"Version":"2012-10-17'
                                          + '","Id":"__default_policy_ID",'
                                          + '"Statement":[{"Sid":"__owner_'
                                          + 'statement","Effect":"Allow",'
                                          + '"Principal":{"AWS":"arn:aws:'
                                          + 'iam::'+accountID+':root"},'
                                          + '"Action":"SQS:*","Resource"'
                                          + ':"arn:aws:sqs:'
                                          + configuration["AWS_DEFAULT_REGION"]
                                          + ':' + accountID + ':'
                                          + configuration["queue_name"]
                                          + '"},{"Sid":"__sender_statement"'
                                          + ',"Effect":"Allow",'
                                          + '"Principal":{"AWS":"*"},"Action"'
                                          + ':"SQS:SendMessage",'
                                          + '"Resource":"arn:aws:sqs:'
                                          + configuration["AWS_DEFAULT_REGION"]
                                          + ':' + accountID + ':'
                                          + configuration["queue_name"]
                                          + '"}]}'
                                          })
    return sqsClient.get_queue_url(QueueName=configuration["queue_name"])




def awsCredentialPreparefile(filecontent, configuration,processorName):
    filecontent = addSensitiveVariable(filecontent, processorName, "Access Key",
                                      configuration["AWS_ACCESS_KEY_ID"])
    filecontent = addSensitiveVariable(filecontent, processorName, "Secret Key",
                                      configuration["AWS_SECRET_ACCESS_KEY"])
    filecontent = addSensitiveVariable(filecontent, processorName, "Region",
                                      configuration["AWS_DEFAULT_REGION"])
    return filecontent


def deleteSQSQueue(configuration):
    sqsClient = boto3.client('sqs',
                             region_name=configuration["AWS_DEFAULT_REGION"])
    queue = sqsClient.get_queue_url(QueueName=configuration["queue_name"])
    response = sqsClient.delete_queue(QueueUrl=queue['QueueUrl'])


def s3NotificationSQS(configuration):
    owner = boto3.client('sts').get_caller_identity().get('Account')
    arn = "arn:aws:sqs:" + configuration["AWS_DEFAULT_REGION"] + ":" + owner \
        + ":" + configuration["queue_name"]
    s3 = boto3.resource('s3')
    bucket_notification = s3.BucketNotification(configuration["AWS_S3_BUCKET"])
    response = bucket_notification.put(
        NotificationConfiguration={
            'QueueConfigurations': [
                {
                    'Id': configuration["AWS_S3_BUCKET"]+"_event",
                    'QueueArn': arn,
                    'Events': [
                        's3:ObjectCreated:*',
                    ],
                },
            ],
        },
        ExpectedBucketOwner=owner,
        SkipDestinationValidation=False)
