
FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1\
    PYTHONPATH="."

COPY . ./

RUN pip3 install --upgrade -r requirements.txt
RUN poetry install
