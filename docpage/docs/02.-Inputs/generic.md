---
sidebar_position: 1
---
# Generic

Generic section creates a ProcessGroup by given a ProcessGroup file, is comprised of:
- An identifier name of the process. It must be unique.
- The path of your ProcessGroup (.json file)
- The variables that compose the workflow (as a list).

```
generic:
  - name: <identifier>
    file: <file-of-process-group>
    variables:
      key: value
      key1: value1
    components:
      - name: InvokeOSCAR
        seconds: 5
```