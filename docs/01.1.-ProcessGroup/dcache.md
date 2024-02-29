# dCache
The main goal of this ProcessGroup is to get the events from dcache.

It is necessary:
- An identifier name of the process. It must be unique.
- Endpoint, user and password
- Folder where active listening
- Statefile is the name of the file that will store the state. Please do not create it with the name `dcache`.

This ProcessGroup is composed of:
- ExecuteProcess
- GetFile


This ProcessGroup only works on the image `ghcr.io/grycap/nifi-sse:latest`


```
dcache:
  - name: dcache
    endpoint: <dcache-endpoint>
    user: <dcache-user>
    password: <dcache-password>
    folder: <input-folder>
    statefile: <file-that-save-state>
    components:
      - name: GetFile
        seconds: 2
```

