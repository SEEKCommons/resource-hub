FROM mcr.microsoft.com/devcontainers/python:3.13-bullseye

COPY requirements.txt /tmp/pip-tmp/

RUN pip3 install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp