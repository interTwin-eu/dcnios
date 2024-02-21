# dCNiOS

[dCache](http://dcache.org) is a system for storing and retrieving huge amounts of data, distributed among a large number of heterogeneous server nodes, under a single virtual filesystem tree with a variety of standard access methods.

[Apache NiFi](http://nifi.apache.org) is a reliable system to process and distribute data through powerful and scalable directed graphs of data routing, transformation, and system mediation logic.

[OSCAR](https://oscar.grycap.net) is an open-source platform for serverless event-driven data processing of containerized applications across the computing continuum.

Together with [dCNiOS](http://github.com/grycap/dcnios) (dCache + NiFi + OSCAR), you can manage the creation of event-driven data processing flows. As shown in the figure, when files are uploaded to dCache, events are ingested in Apache NiFi, which can queue them up depending on the (modifiable at runtime) ingestion rate, to be then delegated for processing into a scalable OSCAR cluster, where a user-defined application based on a Docker image can process the data file.

<img align="right" src="docs/images/dcnios-workflow.png" alt="dCNiOS Workflow" width="400"></left>

Therefore, dCNiOS has been made to interact with NiFi and deploy a complete dataflow. It uses HTTP calls to communicate with a Nifi cluster, which can be automatically deployed by the [Infrastructure Manager (IM)](https://im.egi.eu). Apache NiFi is deployed on a dynamically provisioned Kubernetes cluster running with a custom Docker image named `ghcr.io/grycap/nifi-sse:latest`. This new image includes a client for the [dCache SSE Event Interface](https://www.dcache.org/manuals/UserGuide-8.2/frontend.shtml#storage-events), kindly provided by Paul Millar in [GitHub](https://github.com/paulmillar/dcache-sse). It does not require a Nifi registry.

All the dataflow information is described in a YAML file, and by executing the dCNiOS command-line interface, this dataflow is deployed on Nifi.

From predefined recipes (ProcessGroup in Nifi, .json files) created before,

dCNiOS inserts a general flow and changes the variables to create a concrete workflow.

By default, two process group recipes have been created:


1. dcache, which is an active listener for a dCache instance.  The [Server-sent Events SSE](https://en.wikipedia.org/wiki/Server-sent_events) client actively listens for these events in a user-defined folder in dCache. When a file is uploaded to that folder in dCache, NiFi will introduce the event in the dataflow.
2. InvokeOSCAR, an HTTP call to invoke an OSCAR service asynchronously. OSCAR supports this events specification to let the user decide whether the file should be pre-staged into the execution sandbox to locally process the data within an OSCAR job or to delegate the processing of the event into an external tool, such as a workflow orchestration platform, thus reducing data movements across the systems.


## Getting Started

### Prerequisites

- OSCAR cluster with services deployed
- Nifi Cluster deployed
- A package provider such as [Anaconda](https://www.anaconda.com/)

### Installation

Create an environment with conda and use it.

``` bash
conda create --name dcnios python=3.7.6
conda activate dcnios
```

Install all the requirements defined in `requirements.txt`

``` bash
pip install -r requeriments.txt
```

Or only install the minimal requirements that dCNiOS needs.


``` bash
pip install pyyaml==6.0 requests==2.28.2 oscar_python==1.0.3
```

## Authors

- Germán Moltó mailto:gmolto@dsic.upv.es
- Estibaliz Parcero mailto:esparig@i3m.upv.es
- Sergio Langarita mailto:slangarita@i3m.upv.es

Instituto de Instrumentación para Imagen Molecular (I3M), Centro Mixto CSIC — Universitat Politècnica de València, Camino de Vera s/n, 46022 Valencia, España


## Versions and Maintenance

There is only one version in maintenance:
- The main branch in the source code repository maintains a working state version of the software component.
- Documentation is updated with the new software versions involving any substantial or minimal change in the application's behavior.
- Documentation is updated whenever reported as inaccurate or unclear.

## Licensing

dCNiOS is licensed under the Apache License, Version 2.0. See LICENSE for the full license text.

## Acknowledgements

This work was supported by the project “An interdisciplinary Digital Twin Engine for science’’ (interTwin), which has received funding from the European Union’s Horizon Europe Programme under Grant 101058386.

<img  src="docs/images/inter-twin.png" alt="dCNiOS Workflow" width="200" >

## More

You can find more [information](https://oscar.grycap.net/blog/data-driven-processing-with-dcache-nifi-oscar/ ) in the [OSCAR's blog.](https://oscar.grycap.net/blog/)
