---
sidebar_position: 5
---

# Alterations

The subsection `alterations`, is located inside a Source element and changes the input data format. These alterations are applied as a descendent definition. These steps are helpful to be okay with the input Sources format and to re-use the Sources with no changes.



```
  Kafka:
    - name: kafka
      bootstrap_servers: <ip>:<port>
      topic: <topic>
      group_id: "1"
      sasl_username: <sasl-user>
      sasl_password: <sasl-password>
      ssl_context:
        Truststore_Filename: <name-of-p12>
        Truststore_Password: "<password-of-p12>"
      alterations:
        - action: Merge
          maxMessages: 10
          windowSeconds: 7
        - action: Encode
          Encoding: base64

```
