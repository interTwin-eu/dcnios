---
sidebar_position: 2
---

# Decode

Alteration's Decode decodes the data flow from the chosen encoding. The user must ensure the input data is encoded using the selected encoding.
Three encodes are available: `base64`, `base32` and `hex`. They behave like the command `base64 -d`, `base32 -d`, and hex respectively. For example, If the input data is a string in base64 with the value `aGVsbG8K` or in base32 with the value `NBSWY3DPBI======`. The output data is the same in both cases, `hello`.


Here is the YAML example.


```
alterations:
  - action: Decode
    Encoding: base64
```

Decode Alteration consists of the following component:
-EncodeContent

In this case, DCNiOS uses the same file as the Encode ProcessGroup; it simply changes the configuration.