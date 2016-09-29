FROM python:2.7.11
MAINTAINER Prastut Kumar "kr.prastut@gmail.com"


USER root

ENV home /home

WORKDIR $home

ADD . $home/

EXPOSE 5000

#Install remaining dependencies
ENV CORPORA punkt
ENV AVGTAG averaged_perceptron_tagger
ENV TF_BINARY_URL https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl

#Install all depedencies
RUN pip install -r requirements.txt
RUN pip install --upgrade $TF_BINARY_URL
RUN python /usr/local/lib/python2.7/site-packages/tensorflow/models/image/imagenet/classify_image.py


RUN python -m nltk.downloader $CORPORA
RUN python -m nltk.downloader $AVGTAG

ENTRYPOINT ["./teem_tag.py"]