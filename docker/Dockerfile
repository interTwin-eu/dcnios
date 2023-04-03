FROM apache/nifi:1.20.0
USER root
RUN mkdir /ssefiles
RUN mkdir /state
COPY simple-client.py /ssefiles/simple-client.py
COPY activities.py /ssefiles/activities.py

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install sseclient liboidcagent
