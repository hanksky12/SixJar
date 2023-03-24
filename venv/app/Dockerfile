FROM --platform=$TARGETPLATFORM python:3.9-buster AS builder

WORKDIR /sixJar

COPY requirements.txt /sixJar
RUN  apt-get update && \
     apt-get install -y vim && \
     pip3 install -r requirements.txt


COPY app.py /sixJar
COPY ./app /sixJar/app


CMD python3 app.py
LABEL image_name="sixjar-web"
LABEL version="1.0"
