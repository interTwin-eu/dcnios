---
sidebar_position: 5
---
# Component


The component subsection is used in all Elements like Kafka, OSCAR, and the Generic one. A component alters the workflow's operation by employing Apache NiFi Processors. The Processor's name, execution time and the node on which it runs (ALL or PRIMARY) must be indicated.

## Importance of Process Names

To make effective adjustments, it is necessary to know the names of the Processors that comprise the ProcessGroup. This knowledge enables targeted changes, ensuring that the workflow operates as intended.


## Time Execution

Time execution in Apache NiFi refers to the duration between executions of a Processor within a workflow. This interval determines how often a Processor runs and is crucial for managing resource utilization.

## Node Options

When a Processor is set to run on the ALL node option, it executes on all available nodes in the NiFi cluster. This helps distribute the workload evenly, enhancing parallel processing and improving throughput.

Choosing the PRIMARY node option means the Processor will run only on the designated primary node. This is useful for limiting resource use or maintaining specific configurations that shouldn’t be duplicated across nodes. 



```
    - name: dcache
      endpoint: <dcache-endpoint>
      user: <dcache-user>
      password: <dcache-password>
      folder: <input-folder>
      statefile: <file-that-save-state>
      components:
        - name: GetFile
          seconds: 2
          node: (ALL | PRIMARY)

```