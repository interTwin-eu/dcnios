---
sidebar_position: 2
---

# Decode

Alteration's Decode decodes the data flow from the chosen encoding. The user must ensure the input data is encoded using the selected encoding.
Three encodes are available: `base64`, `base32` and `hex`. It is similar to the command `base64 -d` or `base32 -d`. For example, If the input data is a string in base64 with the value `aGVsbG8K` or in base32 with the value `NBSWY3DPBI======`. The output data will be the same in both cases, `hello`.


Here is the YAML example.


```
alterations:
  - action: Decode
    Encoding: base64
```