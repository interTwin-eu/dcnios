---
sidebar_position: 1
---
# Rucio

Rucio is a Source that listens into a Rucio instance. The following values must be provided:
- An identifier name of the process. It must be unique. Required.
- RabbitMQ host, port, virtual host, and password for the Rucio messaging broker. Required.
- Queue name and service_filter to select Rucio events. Required.

The Rucio Source consists of the following NiFi components:
- ConsumeAMQP
- EvaluateJsonPath
- RouteOnAttribute

```
    RUCIO:
      - name: rucio
        queue_name: events
        host: <rucio-endpoint> #e.g., rucio-intertwin-messaging.desy.de
        port: <rucio-port> #e.g., 5671
        virtual_host: <user-rabbitmq>
        password: <pass-rabbitmq>
        service_filter: rucio-example
        ssl_client_auth: NONE
        ssl_context:
          Truststore_Filename: <truststore-path> #e.g., /opt/nifi/nifi-current/data/truststore.jks
          Truststore_Password: <truststore-pass>
```
