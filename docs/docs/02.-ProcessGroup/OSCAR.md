---
sidebar_position: 5
---

# OSCAR

The goal of this ProcessGroup is to invoke OSCAR services asynchronously:
  - An identifier name of the process. It must be unique.
  - Endpoint
  - Service in OSCAR
  - Token or user/password. The user/password will be first if both authentication processes are defined. Do not edit the OSCAR services.



This ProcessGroup is composed of:
- InvokeOSCAR


```
- name: edgan3
  endpoint: <oscar-endpoint>
  service: <oscar-service>
  token: <token>
  user: <oscar-user>
  password: <oscar-pasword>
```