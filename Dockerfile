FROM python:3.8-slim-buster

ENV PIP_NO_CACHE_DIR 1

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required Packages
RUN apt update && apt upgrade -y
RUN apt-get install -y bash \
            curl \
            git \
            sudo \
            make \
            neofetch \
            postgresql \
            postgresql-client \
            python3-pip \
            python3-requests \
            python3-tz \
            openssl \
            wget ffmpeg \
            opus-tools \
            bpm-tools

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg opus-tools bpm-tools

# Pypi package Repo upgrade
RUN pip3 install --upgrade pip setuptools


# Copy Python Requirements to /root/noxx
WORKDIR /app/

ENV ENV True

# Install requirements
COPY requirements.txt .
RUN sudo pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# Starting Worker
CMD ["python3","-m","noxx"]
