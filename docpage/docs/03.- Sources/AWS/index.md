---
sidebar_position: 5
---
# AWS


**DCNiOS can use some AWS services**: This section clarifies the configuration required to use the credentials!


DCNiOS can use some AWS as input. A valid pair of AWS Access Key and AWS Secret Key is necessary in all those cases. DCNiOS takes the AWS credentials from several places, following a hierarchy. This implementation is made to minimize the times that the credentials are written in the configuration file.

- Environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- From [aws file credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) with the `default` section. Here is an example:
   ``` bash
   [default]
   aws_access_key_id = AK<>
   aws_secret_access_key = <>
   ```
- From the DCNiOS workflow file using the argument `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.



AWS_DEFAULT_REGION is mandatory for any that uses AWS in the configuration file. These ProcessGroups use AWS credentials:
- [SQS](/docs/Sources/AWS/SQS)
- [S3](/docs/Sources/AWS/S3)

