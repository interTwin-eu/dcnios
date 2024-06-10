---
sidebar_position: 5
---
# Generic

The generic section creates a custom workflow by giving a ProcessGroup file (.json). The purpose of this component could be Source, Destination, Alteration, or even a data flow complete. The behavior is specific by the creator of the file '.json'

which is comprised of:
- An identifier name of the process. It must be unique. Required.
- The path of your ProcessGroup (.json file).Required.
- The variables that compose the workflow (as a list).


```
generic:
 - name: <identifier>
   file: <file-of-process-group>
   variables:
     key1: value1
     key2: value2
   components:
     - name: InvokeOSCAR
       seconds: 5
```



