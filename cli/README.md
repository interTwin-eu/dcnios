# DcNiOs

## Yaml structure

There are five sections in this FDL; two define a concrete Nifi processgroup `dcache.json` and `InvokeOSCAR.json`.

1. First section indicates the Nifi credentials:
    - Endpoint, user and password

2. Second section, dcache. It uses the `dcache.json` file that gets the events from dcache. It is necessary:
    - An identifier name of the process. It must be unique.
    - Endpoint, user and password
    - Folder where active listening
    - Statefile is the variable that will create a file to save listening state. Please, do not create it with the name `dcache`.

3. Third section, oscar. It uses an `InvokeOSCAR.json` file that invokes a service OSCAR asynchronous:
    - An identifier name of the process. It must be unique.
    - Endpoint
    - Service in OSCAR
    - Token or user/password. In case both authentication processes are defined, user/password will apply. Do not edit the OSCAR services.
    - In this case, the section of components has been added. This section has made to change the data ingestion on the OSCAR cluster. It needs the name of the process and the seconds that will be between interactions. The name defined in the `InvokeOSCAR.json` file by default is `InvokeOSCAR`.

4. Fourth section, generic. This section imports all kinds of processgroup.
    - name
    - file
    - variables

5. Last section create the connection between process using identifiers names
    - from (dcache identifier)
    - to (OSCAR invocation identifier)

Inside of dcache, oscar and generic sections, a subsection `components` has been created to change the configuration of a process, right now it changes the schedule time and execution node execution, where you can choose which node is going to be executed in all nodes or the primary node.

## Manage the dataflow with commands

Once the dataflow is defined in the YAML file, its time to create it with the command:

``` bash
python dcnios-cli.py apply -f description.yaml
```

To start or stop all the processgroup defined in the YAML:

``` bash
python dcnios-cli.py [start | stop] -f description.yaml
```

To delete all the processgroup defined in the YAML:

``` bash
python dcnios-cli.py delete -f description.yaml
```

### Change Schedule time

A command has been created to change the time of a process between execution:

``` bash
python dcnios-cli.py changeSchedule --host={nifi-endpoint} \
--user={user} --password={pass}  \
--processGroup={processGroupName} --component={defined_in_template} \
--seconds=10
```
