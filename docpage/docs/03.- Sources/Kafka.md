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
- If the consumed topic follows a `key:value` pattern, set the argument `separate_by_key` true and select the demarcator with `message_demarcator`.

An SSL connection between NiFi and Kafka is necessary. A PKCS12 certificate and the certificate's password must be provided.


Kafka Source consists of the following component:
- ConsumeKafka_2_6

```
  Kafka:
    - name: kafka
      bootstrap_servers: <ip>:<port>
      topic: <topic>
      group_id: "1"
      sasl_username: <sasl-user>
      sasl_password: <sasl-password>
      #separate_by_key: "false"
      #message_demarcator: ";"
      ssl_context:
        Truststore_Filename: <name-of-p12>
        Truststore_Password: "<password-of-p12>"
```
