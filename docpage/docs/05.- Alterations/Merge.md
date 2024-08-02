---
sidebar_position: 3
---

# Merge

Alteration's Merge put together some messages in one. There are two variables to set: the maximum messages `maxMessages` can get and the waiting window time `windowSeconds`.
The final output will aggregate the input messages separated by a lane break. If the receive data order is `I am the message 1` and `I am the message 2` the output will be:

```
I am the message 1
I am the message 2
```

Here is the YAML example.


```
alterations:
  - action: Merge
    maxMessages: 10
    windowSeconds: 2
```