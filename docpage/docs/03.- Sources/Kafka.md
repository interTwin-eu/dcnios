---
sidebar_position: 2
---
# Kafka



The Kafka Source allows us to consume a Kafka topic. It requires this information:
- An identifier name of the process. It must be unique. Required.
- Kafka bootstrap_servers, just the IP and the port with any protocol as `<ip>:<port>`. Required.
- The topic name that is going to be consumed. Required.
- The group identifier indicates the consumer group. Required.
- [IM](https://www.grycap.upv.es/im/index.php) serve a recipe that supports the SASL_SSL security protocol. So, the user `sasl_username` and password `sasl_password` must be set. These parameters are set at Kafka deployment time. Required.
- In case the topics you are consuming follow a `key:value` pattern set the argument `separate_by_key` as true and select the demarcator with `message_demarcator`

Also, it is necessary an SSL connection between NiFi and Kafka. This connection is made by a PKCS12 certificate and the password of the certificate.

```
Kafka:
- name: kafka
   bootstrap_servers: <ip>:<port>
   topic: <kafka-topic-name>
   group_id: "<kafka-group-id>"
   sasl_username: <kafka-sasl-user>
   sasl_password: <kafka-sasl-password>
   ssl_context:
     Truststore_Filename: <certificate-file.p12>
     Truststore_Password: <certificate-file-password>
```
