---
sidebar_position: 2
---

# Users Guide

This page explains the main concepts of DCNiOS, such as the DCNiOS commands and workflow definition.

## Commands


Create a workflow with the command apply.	
```
python dcnios-cli.py apply -f description.yaml
```

Start or stop the workflow.
```
python dcnios-cli.py [start | stop] -f description.yaml
```

Delete the workflow with the command delete. 
```
python dcnios-cli.py delete -f description.yaml
```

Edit the scheduling time for a process:

```
python dcnios-cli.py changeSchedule --host={nifi-endpoint} \
--user={user} --password={pass}  \
--processGroup={processGroupName} --component={defined_in_template} \
--seconds=10
```






## File workflow configuration structure (Yaml structure)

Here, we explain the workflow definition, the structure of the configuration file, and the information the user has to know about each third-party connection. DCNiOS deploys and configures all the definitions in Apache NiFi.

### Apache NiFi credentials:

In this `nifi` section, set the Apache NiFi credentials. Inside this section, define the workflow.

```
nifi:
 endpoint: https://<nifi-endpoint>
 user: <nifi-user>
 password: <nifi-password>
```


### Sources, Destinations and Alterations

Moreover, it is necessary to define the source and destination of data.

Sources:
- [dCache](/docs/Sources/dcache)
- [KAFKA](/docs/Sources/Kafka)
- [S3](/docs/Sources/AWS/S3)
- [SQS](/docs/Sources/AWS/SQS)

Destinations:
- [OSCAR](/docs/Destinations/OSCAR)


The input data format from Sources can change using Alterations.

Alterations:
- [Merge](/docs/Alterations/Merge)
- [Encode](/docs/Alterations/Encode)
- [Decode](/docs/Alterations/Decode)


#### Components Subsection

The components subsection changes the behavior of an inter-process. When you deploy an element, there are some processes running in the background. You can change the seconds between executions (execution ratio) and select which node will perform the execution (PRIMARY or ALL). However, it is necessary to know the name of the process. For example, the destination OSCAR has the component InvokeOSCAR, which sends an HTTP call.


```
components:
- name: InvokeOSCAR
  seconds: 2
  node: (ALL | PRIMARY)
```


#### Alterations

[Alterations](/docs/Alterations), located inside [Sources](/docs/Sources), are employed to modify the format of data. The alterations are applied in the specified order. In the following example, the input data is merged into one message. Then, the merged message is encoded in base64 format.


```
  - action: Merge
    maxMessages: 10
    windowSeconds: 7
  - action: Encode
    Encoding: base64
```

### Connections

The Connections section defines the links between Sources and Destinations.

```
connection:
  - from: dcache
    to: edgan3
```



### Example


```
nifi:
 endpoint: https://<nifi-endpoint>
 user: <nifi-user>
 password: <nifi-password>
 dCache:
   - name: dcache
     endpoint: <dcache-endpoint>/api/v1
     user: <dcache-user>
     password: <dcache-password>
     folder: <dcache-input-folder>
     statefile: <file-that-save-state>
 OSCAR:
   - name: edgan3
     endpoint: <oscar-endpoint>
     service: <oscar-service>
     token: <oscar-token>
 connection:
   - from: dcache
     to: edgan3
```
