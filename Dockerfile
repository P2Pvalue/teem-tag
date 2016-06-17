FROM python:2.7.6
MAINTAINER Prastut Kumar "kr.prastut@gmail.com"

RUN apt-get install -y wget git-core

USER root

#Install NLTK
