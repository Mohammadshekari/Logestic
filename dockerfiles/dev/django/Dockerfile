FROM python:3.10-slim-buster

LABEL maintainer="bigdeli.ali3@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# RUN sed -i 's/http:\/\/[a-zA-Z0-9]*.[a-zA-Z0-9]*.*.com/http:\/\/ir.ubuntu.sindad.cloud/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin \
    postgresql-client \
    postgresql-server-dev-all \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt  \
    && pip install debugpy 

COPY ./core .

#create a non root user to access the container 
RUN adduser -u 5678 --disabled-password --gecos "" vscode