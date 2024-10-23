---
sidebar_position: 5
---
# Component


Component subsection is use in all Elements like Kafka, OSCAR or a Generic one. This subsection changes key parts of the workflow's operation. However, it is necessary to know the names of the Process that make up the ProcessGroup. By indicating the name of the Process, you can change the execution time and the node on which it runs (ALL or PRIMARY).

## Importance of Process Names

To make effective adjustments, it is necessary to know the names of the Processes that comprise the ProcessGroup. This knowledge enables targeted changes, ensuring that the workflow operates as intended.


## Time Execution

Time execution in Apache NiFi refers to the duration between executions of a Process within a workflow. This interval determines how often a Process runs and is crucial for managing resource utilization.

## Node Options

When a Process is set to run on the ALL node option, it executes on all available nodes in the NiFi cluster. This helps distribute the workload evenly, enhancing parallel processing and improving throughput.

Choosing the PRIMARY node option means the Process will run only on the designated primary node. This is useful for limiting resource use or maintaining specific configurations that shouldn’t be duplicated across nodes. 



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