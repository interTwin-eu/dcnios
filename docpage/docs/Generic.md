---
sidebar_position: 8
---

# Generic Element


In this document, we focus on the concept of Generic Elements within NiFi, specifically how to deploy custom workflows using already created ProcessGroup files. Understanding these elements is essential for efficiently managing and automating data flows in Apache NiFi.


The generic section creates a custom workflow by providing a ProcessGroup file (.json). The purpose of this element could be Source, Destination, Alteration, or even a complete data flow. The author of the file '.json' sets the purpose of the workflow. For the use of Generic Element, it is necessary to have knowledge in creating ProcessGroups in Apache NiFi.

DCNiOS creates the specified workflow in Apache NiFi using the .json file, substitutes the environment variables, and uses the same configuration characteristics as other Elements such as Connections and Components. Additionally, make the connections with other Elements. Thus, the declarative .yaml file has the following structure:

- An identifier name of the process. It must be unique. Required.
- The path of your ProcessGroup (.json file).Required.
- The variables that compose the workflow (as a list).

Also, a generic element can use [Alterations](/docs/Alterations) if it is connected with another element, or the subsection `component` to modify the time execution or the node execution. The user must know the names of the NiFi Processor defined in the .json.

To use a Generic Element that interacts with other elements, it is necessary to use an Input or Output port with the default name. Please use only one Input and one Output.



```
generic:
 - name: <identifier>
   file: <file-of-process-group>
   variables:
     key1: value1
     key2: value2
   components:
     - name: GetFile
       seconds: 2
       node: (ALL | PRIMARY)
   alterations:
     - action: Encode
       Encoding: base64

```

