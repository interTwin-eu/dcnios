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
from apis import aws
import env



def createPutS3(nifiConfiguration,s3Info,s3content):
    if "MinIO_Endpoint" in s3Info:
        auxiliaryFunctions.addSensitiveVariable(s3content, "PutS3Object", "Endpoint Override URL", s3Info["MinIO_Endpoint"])
        s3Info[env.AWS_DEFAULT_REGION_TAG]="us-east-1"
    else:
        aws.getAWSCredentials(s3Info)
    s3content = aws.awsCredentialPreparefile(s3content, s3Info,"PutS3Object")
    auxiliaryFunctions.addSensitiveVariable(s3content, "PutS3Object", "Bucket", s3Info[env.AWS_S3_BUCKET_TAG])
    nifiConfiguration.create(s3Info[env.NAME_TAG], s3content)
 