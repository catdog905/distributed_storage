FROM python:alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1\
    PYTHONPATH="."

COPY . ./

RUN pip install poetry
RUN pip install grpcio
RUN pip install protobuf
RUN poetry install