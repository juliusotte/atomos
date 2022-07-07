FROM python:3.9-slim-buster

COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

RUN mkdir /source/
COPY source/ /source/
RUN pip install -e /source/
COPY tests/ /tests/

WORKDIR /source/