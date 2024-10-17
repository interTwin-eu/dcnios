---
sidebar_position: 4
---
# SQS


SQS Source consumes from an AWS SQS queue. It creates an SQS in creation time, requiring:
- An identifier name of the process. It must be unique. Required.
- The region where the SQS is going to be deployed. AWS_DEFAULT_REGION Required.
- The queue name. Required.


Here is an example of the configuration file. Check the documentation of [AWS credentials](/dcnios/docs/AWS) to define the Access Key and Secret Key.


```
SQS:
 - name: sqs
   AWS_DEFAULT_REGION: <aws-region>
   queue_name: <aws-queue-name>
```
