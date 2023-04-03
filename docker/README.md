# New Image of Nifi

It had created a Docker image called `ghcr.io/grycap/dcnios:latest` from apache/nifi version 1.20.0.
Also, it created two folders /ssefiles and /state.

1. The /ssefiles folder has introduced the files necessary to execute the [sse protocol](https://github.com/paulmillar/dcache-sse) defined in the paulmillar GitHub repository.
2. The other folder /state will be a persistent folder that will save all the events and the state.

Finally, all the dependencies necessary to execute the sse protocol have been added.
