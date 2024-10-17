---
sidebar_position: 1
---
# dCache

dCache is a Source that listens into a dCache instance. The following values must be provided:
- An identifier name of the process. It must be unique. Required.
- Endpoint, user, and password of a dCache instance. Required.
- Folder of dCache where keeps an active listening.Required.
- Statefile is the file that will store the state. Please, do not employ `dcache` as its name, as it may cause problems. Required.

The dCache Source only works when the NiFi cluster is deployed with the image `ghcr.io/grycap/nifi-sse:latest`, is composed of:
- ExecuteProcess
- GetFile

```
dCache:
 - name: dcache
   endpoint: <dcache-endpoint>
   user: <dcache-user>
   password: <dcache-password>
   folder: <dcache-input-folder>
   statefile: <file-that-save-state>
   components:
     - name: GetFile
       seconds: 2
```
