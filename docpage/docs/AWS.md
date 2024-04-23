---
sidebar_position: 4
---
# AWS

> :warning: **DCNiOS can use some AWS services**: This section clarifies the configuration required to use the credentials!

DCNiOS can use some AWS as input. A valid pair of AWS Access Key and AWS Secret Key is necessary in all those cases.

- DCNiOS takes the credentials from the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- If those environment variables do not exist, the credentials are taken from [aws file credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) with the `default` section. Here is an example:
    ``` bash
    [default]
    aws_access_key_id = AK<>
    aws_secret_access_key = <>
    ```
- If DCNiOS does not successfully use the credentials as environment variables or in the credential file.
DCNiOS gets them from configuration files named `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
This implementation is made to minimize the times that the credentials are written in the configuration file.

AWS_DEFAULT_REGION is mandatory in any source that uses AWS of the configuration file. Right now, the ProcessGroup that uses AWS credentials are:
- [SQS](/docs/Inputs/SQS)
- [S3](/docs/Inputs/S3)