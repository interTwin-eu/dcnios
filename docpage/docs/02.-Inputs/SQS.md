---
sidebar_position: 5
---
# SQS

SQS is the ProcessGroup that consumes an AWS SQS queue , is comprised of:
The main purpose is to get as input the data from a SQS. So, this section will create an SQS in AWS and a processGroup in the Nifi cluster.
 - An identifier name of the process. It must be unique.
 - The region where the SQS is going to be deployed. AWS_DEFAULT_REGION
 - The queue name.

Here is an example of the configuration file. Check the documentation of [AWS credentials](/dcnios/docs/AWS) to define the Access Key and Secret Key.

```
SQS:
  - name: sqs
    AWS_DEFAULT_REGION: <aws-region>
    queue_name: <queue-name>
```