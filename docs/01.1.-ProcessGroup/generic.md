# Generic

The generic section is made to deploy your ProcessGroups.
Need to be defined:
- The identifier name
- The path of your processGroup (.json file)
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