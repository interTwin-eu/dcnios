FROM apache/nifi:1.20.0
USER root
RUN mkdir -p /ssefiles /state

COPY ["simple-client.py", "activities.py", "/ssefiles" ]

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install sseclient liboidcagent  && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && rm -rf ~/.cache/
