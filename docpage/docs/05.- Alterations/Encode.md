---
sidebar_position: 1
---

# Encode

Alteration's Encode changes the data flow to the chosen encoding. Three encodings are available: `base64`, `base32` and `hex`. It is similar to the command `base64` `base32` or `hexdump`. 
For example, If the input data is a string with the message `hello`. The output message encode in base64 is `aGVsbG8K`, in base32 is `NBSWY3DPBI======` and in hex `0000000 6568 6c6c 0a6f 0000006`

Here is the YAML example.

```
alterations:
  - action: Encode
    Encoding: base64
```


Encode Alteration consists of the following component:
- EncodeContent