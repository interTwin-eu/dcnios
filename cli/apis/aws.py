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
import env
from apis import auxiliaryFunctions


def getAWSCredentials(configuration):
    if env.AWS_ACCESS_KEY_ID_TAG in os.environ and os.environ[env.AWS_ACCESS_KEY_ID_TAG] != "" \
        and env.AWS_SECRET_ACCESS_KEY_TAG in os.environ \
            and os.environ[env.AWS_SECRET_ACCESS_KEY_TAG] != "":
        print("AWS Credentials: Credentials from environment")
        configuration[env.AWS_ACCESS_KEY_ID_TAG] = os.environ[env.AWS_ACCESS_KEY_ID_TAG]
        configuration[env.AWS_SECRET_ACCESS_KEY_TAG] = \
            os.environ[env.AWS_SECRET_ACCESS_KEY_TAG]
    elif os.path.exists(os.environ["HOME"] + "/.aws/credentials"):
        print("AWS Credentials: Credentials from credentials file")
        session = boto3.Session(profile_name="default")
        credentials = session.get_credentials()
        configuration[env.AWS_ACCESS_KEY_ID_TAG] = credentials.access_key
        configuration[env.AWS_SECRET_ACCESS_KEY_TAG] = \
            credentials.secret_key
    elif env.AWS_ACCESS_KEY_ID_TAG in configuration \
            and env.AWS_SECRET_ACCESS_KEY_TAG in configuration:
        print("AWS Credentials: Credentials from configuration file")


def createSQSQueue(configuration):
    accountID = boto3.client('sts').get_caller_identity().get('Account')
    sqsClient = boto3.client('sqs',
                             region_name=configuration[env.AWS_DEFAULT_REGION_TAG])
    response = sqsClient.create_queue(QueueName=configuration[env.QUEUE_NAME_TAG],
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
                                          + configuration[env.AWS_DEFAULT_REGION_TAG]
                                          + ':' + accountID + ':'
                                          + configuration[env.QUEUE_NAME_TAG]
                                          + '"},{"Sid":"__sender_statement"'
                                          + ',"Effect":"Allow",'
                                          + '"Principal":{"AWS":"*"},"Action"'
                                          + ':"SQS:SendMessage",'
                                          + '"Resource":"arn:aws:sqs:'
                                          + configuration[env.AWS_DEFAULT_REGION_TAG]
                                          + ':' + accountID + ':'
                                          + configuration[env.QUEUE_NAME_TAG]
                                          + '"}]}'
                                          })
    return sqsClient.get_queue_url(QueueName=configuration[env.QUEUE_NAME_TAG])


def awsCredentialPreparefile(filecontent, configuration, processorName):
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, processorName, "Access Key",
                                                          configuration[env.AWS_ACCESS_KEY_ID_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, processorName, "Secret Key",
                                                          configuration[env.AWS_SECRET_ACCESS_KEY_TAG])
    filecontent = auxiliaryFunctions.addSensitiveVariable(filecontent, processorName, "Region",
                                                          configuration[env.AWS_DEFAULT_REGION_TAG])
    return filecontent


def deleteSQSQueue(configuration):
    sqsClient = boto3.client('sqs',
                             region_name=configuration[env.AWS_DEFAULT_REGION_TAG])
    queue = sqsClient.get_queue_url(QueueName=configuration[env.QUEUE_NAME_TAG])
    response = sqsClient.delete_queue(QueueUrl=queue['QueueUrl'])


def s3NotificationSQS(configuration):
    owner = boto3.client('sts').get_caller_identity().get('Account')
    arn = "arn:aws:sqs:" + configuration[env.AWS_DEFAULT_REGION_TAG] + ":" + owner \
        + ":" + configuration[env.QUEUE_NAME_TAG]
    s3 = boto3.resource('s3')
    bucket_notification = s3.BucketNotification(configuration[env.AWS_S3_BUCKET_TAG])
    response = bucket_notification.put(
        NotificationConfiguration={
            'QueueConfigurations': [
                {
                    'Id': configuration[env.AWS_S3_BUCKET_TAG]+"_event",
                    'QueueArn': arn,
                    'Events': [
                        's3:ObjectCreated:*',
                    ],
                },
            ],
        },
        ExpectedBucketOwner=owner,
        SkipDestinationValidation=False)
