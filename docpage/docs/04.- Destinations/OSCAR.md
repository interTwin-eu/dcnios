---
sidebar_position: 1
---
# OSCAR


The OSCAR Destination invokes an OSCAR service asynchronously:
- An identifier name of the process. It must be unique. Required.
- Endpoint. Required.
- Service in OSCAR. Required.
- Token or user/password. The user/password has priority. Do not edit the OSCAR services. Required.


Destination is composed of this component:
- InvokeOSCAR



```
- name: edgan3
  endpoint: <oscar-endpoint>
  service: <oscar-service>
  token: <oscar-service-token>
  user: <oscar-user>
  password: <oscar-pasword>
```
