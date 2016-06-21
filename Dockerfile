FROM python:2.7.11
MAINTAINER Prastut Kumar "kr.prastut@gmail.com"


USER root

ENV home /home

WORKDIR $home

ADD . $home/


#Install all depedencies
RUN pip install -r requirements.txt

#Install remaining dependencies
ENV CORPORA punkt
ENV AVGTAG averaged_perceptron_tagger

RUN python -m nltk.downloader $CORPORA
RUN python -m nltk.downloader $AVGTAG

CMD ["python","teem_tag.py"]