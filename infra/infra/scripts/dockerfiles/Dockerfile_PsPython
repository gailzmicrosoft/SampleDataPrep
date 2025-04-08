# Use a base image with Azure CLI
FROM mcr.microsoft.com/azure-cli:2.52.0

# Install Python 3.11.9
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-distutils python3.11-venv && \
    apt-get clean

# Set Python 3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Verify installations
RUN az --version
RUN python3 --version
RUN pip3 --version
