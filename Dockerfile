FROM python:2.7.11
MAINTAINER Prastut Kumar "kr.prastut@gmail.com"


USER root

RUN apt-get install -y git 
RUN git clone https://github.com/P2Pvalue/teem-tag.git

EXPOSE 5000

WORKDIR /teem-tag

#Install all depedencies
RUN pip install -r requirements.txt


#Install remaining dependencies
ENV CORPORA punkt
ENV AVGTAG averaged_perceptron_tagger

RUN python -m nltk.downloader $CORPORA
RUN python -m nltk.downloader $AVGTAG

ENTRYPOINT ["./teem_tag.py"]