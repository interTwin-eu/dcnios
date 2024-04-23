---
sidebar_position: 3
---
# Kafka

Kafka is the ProcessGroup that consumes a Kafka topic, is comprised of:
 - An identifier name of the process. It must be unique.
 - Kafka endpoint, just the IP and the port with any protocol as `<ip>:<port>`
 - The topic name which is going to be consumed. Required.
 - The group identifier indicating the consumer group. Required.
 - In case the Kafka topics are separated by `key:value` set the argument `separate_by_key` as true and select the demarcator with `message_demarcator`:
    - separate_by_key
    - message_demarcator
 - The kafka recipe in [IM](https://www.grycap.upv.es/im/index.php) support the SASL_SSL security protocol. So, the user and password of the SASL_SSL security protocol must be set:
    - sasl_username: `user`
    - sasl_password: `password`


The connection between NiFi and Kafka employs SSL context,the SSL Protocol used by default is TLS, and the Truststore Type is PKCS12. SSL context only needs the Truststore filename and Truststore password. The Truststore file must be under "/opt/nifi/nifi-current/data/" directory.


```
Kafka:
- name: kafka
    bootstrap_servers: <ip>:<port>
    topic: test
    group_id: "1"
    sasl_username: user
    sasl_password: pass
    ssl_context:
      Truststore_Filename: "file_of_pkcs12.p12"
      Truststore_Password: "the-password"
```