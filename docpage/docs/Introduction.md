---
sidebar_position: 1
---

# Introduction

DCNiOS is an open-source command-line tool that easily manages the creation of event-driven data processing flows. DCNiOS reads a file with a workflow defined in a YAML structure. Then, DCNiOS creates this workflow in an Apache NiFi cluster. DCNiOS uses transparently the Apache NiFi [ProcessGroups](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html#Configuring_a_ProcessGroup) to create predefined workflows.


![DCNiOS images](../static/img/dcnios-logo-hor.png)

Apache NiFi ProcessGroup is a group of Processors that compose a dataflow. DCNiOS uses predefined ProcessGroups that make simple actions like interacting with third-party elements (e.g., consuming from Kafka) or changing the data content (e.g.encoding the data in base64) to compose a complete dataflow. 

In DCNiOS documentation, the ProcessGroups are split by purpose into three main groups: 'Sources', 'Destinations', and 'Alterations'.
- 'Sources' interact with third-party elements as the input data receiver.
- 'Destinations' interact with third-party elements as an output data sender.
- 'Alterations' that do not interact with third-party elements and change the format of the data flow.



# Getting Started

## Prerequisites

- OSCAR cluster containing the user-defined OSCAR Services. You can see some [examples](https://github.com/grycap/oscar/tree/master/examples) in GitHub.
- Apache NiFi cluster deployed.
- A Python distribution such as [Anaconda](https://www.anaconda.com/) or Python version 3.7.6
- An input source (e.g.: dCache, Kafka, S3 AWS, SQS AWS)


[IM](https://www.grycap.upv.es/im/index.php) can deploy a Kubernetes cluster that includes an OSCAR cluster and Apache NiFi.


## Installation

1. Download the repository in a local folder.

    ``` bash
    git clone git@github.com:interTwin-eu/dcnios.git
    cd dcnios
    ```

2. Set up a virtual environment (optional but recommended):

    You can choose between Conda or Venv for managing Python dependencies.

    #### Using Conda

    Create a new Conda environment and activate it:

    ``` bash
    conda create --name dcnios python=3.7.6
    conda activate dcnios
    ```

    #### Using Venv

    Create a virtual environment with Venv and activate it:

    ``` bash
    python -m venv dcniosenv
    source dcniosenv/bin/activate
    ```

3. Install Dependencies

    Install all the required dependencies listed in requirements.txt:

    ``` bash
    pip install -r requirements.txt
    ```

    Alternatively, you can install the minimum required dependencies for DCNiOS:

    ``` bash
    pip install pyyaml==6.0 requests==2.28.2 oscar_python==1.0.3
    ```
4. Verify Installation

    Once you've installed the dependencies. You can verify this by running a simple Python script. Try the following Python command to check if the packages are installed correctly:

    ``` bash
    python -c "import yaml, requests, oscar_python; print('All dependencies are correctly installed.')"
    ```
