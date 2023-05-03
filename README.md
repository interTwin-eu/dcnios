# DcNiOs

This repository has been made to interact with Nifi and deploy a complete dataflow. It uses HTTP calls to communicate with a Nifi cluster deployed by IM. It does not need a Nifi registry.

All the dataflow information will be described in a YAML file, and by executing dcnios-cli, this dataflow will be deployed on Nifi.
From predefined recipes (ProcessGroup in Nifi, .json files) created before,
dCNiOs will insert a general flow and change the variables to create a concrete workflow.
By default, two process group recipes have been created before:

1. dcache, which is an active listen in dcache. In this case, where we will listen in dcache, we will deploy a Nifi cluster with a custom Docker image named `ghcr.io/grycap/dcnios:latest`. This new image includes client for the [dCache SSE Event Interface](https://www.dcache.org/manuals/UserGuide-8.2/frontend.shtml#storage-events), kindly provided by Paul Millar in [Github](https://github.com/paulmillar/dcache-sse).  The sse protocol creates an active listening that will be used in a folder of dcache. When an event occurs in dcache, Nifi will get and introduce it in the dataflow.
2. InvokeOSCAR, an HTTP call to invoke an OSCAR service asynchronously.

## Set environment

Create an environment with conda and use it.

``` bash
conda create --name dcnios python=3.7.6
conda activate dcnios
```

Install all the requirements defined in `requirements.txt`

``` bash
pip install -r requeriments.txt
```

Or only install the minimal requirements that dCNiOs needs.

``` bash
pip install pyyaml==6.0 requests==2.28.2 oscar_python==1.0.3
```
