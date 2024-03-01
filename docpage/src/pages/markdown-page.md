---
title: Main Page
---


DCNiOS is an open-source command-line tool to easily manage the creation of event-driven data processing flows.
DCNiOS, Data Connector through [Apache NiFi](https://nifi.apache.org/) for [OSCAR](https://oscar.grycap.net/), facilitates the creation of event-driven processes connecting a Storage System like [dCache](https://www.dcache.org/) to a scalable OSCAR cluster by employing predefined dataflows that are processed by Apache NiFi.


DCNiOS was developed within the interTwin project. DCNiOS captures events, queues them up in a Nifi dataflow, and ingests them in an OSCAR cluster at a customized rate, where an OSCAR service is run based on a user-defined application (containerized in a Docker image). 

The DCNiOS command-line application is available in the Source Code repository. Additionally, the corresponding TOSCA templates and the ansible roles that are required to deploy an Apache Nifi cluster via the Infrastructure Manager (IM) have been provided. Any user can self-deploy such a cluster via the [IM Dashboard](https://im.egi.eu).
























