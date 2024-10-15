# Regarding the Docker image

A Docker image called `ghcr.io/grycap/nifi-sse:latest` has been created from Apache NiFi version 1.20.0.

The image contains two folders called *ssefiles* and *state*.

1. The *ssefiles* folder contains the necessary files to execute the [dCache SSE protocol](https://github.com/paulmillar/dcache-sse) as defined in the paulmillar GitHub repository.
2. The *state* folder purpose is to be employed as a persistent storage for the events and the state.

The image also contains preinstalled the required dependencies to execute the SSE protocol.
