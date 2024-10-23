---
sidebar_position: 7
---

# Connections

The Connections section defines the links between Sources and Destinations. It is declared at the same level as Source and Destination, and you have to use the identifier name of the Element to create the connection.The use of [Alterations](/docs/Alterations) does not affect the connection between the elements; the connection is made transparently.

Connections play a crucial role in managing the flow of data between different elements of the workflow, ensuring the order and integrity of the data. By utilizing Connections, workflows can be designed in a modular fashion, allowing for easy modifications—such as adding or removing components—without disrupting the overall flow.

```
  OSCAR:
    - name: OSCAROutput 
  Kafka:
    - name: kafkaInput
  connection:
    - from: kafkaInput
      to: OSCAROutput
```
