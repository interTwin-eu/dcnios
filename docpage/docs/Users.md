---
sidebar_position: 2
---

# Users Guide

Here, you will find an explanation of the main concepts of DCNiOS, such as the DCNiOS commands, how to define a workflow, involved sections, and the commun sections for all the third-party connections.

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

Here, we will explain the workflow definition, the structure of the configuration file, and the information the user has to know about each third-party connection. DCNiOS deploys and configures all the definitions in Apache NiFi.

### Apache NiFi credentials:

In this 'nifi' section, the Apache NiFi credentials will be defined. Inside this section will be defined the Sources that will be deployed and the conection between them.

```
nifi:
 endpoint: https://<nifi-endpoint>
 user: <nifi-user>
 password: <nifi-password>
```


### Sources, Destinations and Alterations

Moreover, it is necessary to define the source and destination of data.

Sources:
- [dCache](https://www.dcache.org/)
- [KAFKA](https://kafka.apache.org/)
- [S3](https://aws.amazon.com/es/s3/)

Destinations:
- [OSCAR](https://oscar.grycap.net/)

Alterations:
- Merge
- Encoded
- Decoded


#### Components Subsection

The subsection `components`, inside Sources and Destinations,  is employed to change the configuration of a single Processor of Apache NiFi. It is necessary to know the name of the component. Then, we can change the seconds between executions,
the scheduled time, seconds between executions (ratio execution), and in which kind of node in Nifi is going to execute.the node execution can be changed.




```
components:
- name: GetFile
  seconds: 2
  node: (ALL | PRIMARY)
```


#### Alterations

The subsection `alterations`, inside Sources, change the data format. These alterations are applied as a descendent definition. In this example, the input data is merged into one message. Then, the merge message is encoded.

```
  - action: Merge
    maxMessages: 10
    windowSeconds: 7
  - action: Encode
    Encoding: base64
```

### Connections



In the Connections section, the connections between sources and destinations are established by employing the `from` and `to` keys.

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
