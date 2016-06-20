FROM python:2.7.11
MAINTAINER Prastut Kumar "kr.prastut@gmail.com"


USER root

ENV home /home

WORKDIR $home

ADD . $home/


#Install all depedencies
RUN pip install -r requirements.txt

CMD ["python","teem_tag.py"]