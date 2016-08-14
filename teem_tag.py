#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
from flask import Flask, request
from urlparse import urljoin
import os, sys, pickle, pymongo, json, requests, logging

# Initialising Flask. Webserver to handle POST from SwellRT. 
app = Flask(__name__)
# SwellRT IP. Works only with docker-compose setup.
swellrt_host = os.environ.get('SWELLRT_HOST')

if swellrt_host:
    swellrt = 'http://' + swellrt_host +':9898/swell/'
else:
    swellrt = 'http://swellrt:9898/swell/'

session = False


# For authentication. Defaults to: username = teemtag@local.net, password = teemtag
tag_user = os.environ.get('TEEMTAG_USERNAME')
tag_pwd = os.environ.get('TEEMTAG_PASSWORD')



@app.route("/", methods=['GET', 'POST'])
def tags():

    

    if request.method == 'POST':

        global session

        if not session:
            session = authfromSwellRT()

        data = request.get_json()
        
        #Initialisation for context
        wave_id = data['waveid']
        description = data['data']['text']

        tags = json.dumps(mytagger(data['data']['text'],10), default=lambda x: str(x).strip('"\''))
       
        #For logs
        app.logger.info(tags)
        
        post2swellRT(session,wave_id,tags)
        
        return json.dumps(True)
    else:
        tags = json.dumps("Hello from Teem Tag",10, default=lambda x: str(x).strip('"\''))
        return tags



def authfromSwellRT():
    session = requests.session()
    swellrt_auth_link = urljoin(swellrt,'auth')

    try:

        if tag_user and tag_pwd:
            session.post(swellrt_auth_link, json={"id": tag_user,"password": tag_pwd})
        else:
            session.post(swellrt_auth_link, json={"id":"teemtag@local.net","password":"teemtag"})
    except requests.exceptions.RequestException as e:    
        app.logger.error('Authentication failed from SwellRT')

    try:
        auth_test = session.get(swellrt_auth_link)
    except requests.exceptions.RequestException as e:    
        app.logger.error('Authentication checking failed')
    
    if auth_test.status_code == 200:
        app.logger.info('Succesful Authentication')
        return session
    else:
        app.logger.error('Cannot authenticate from SwellRT. Exiting!')


def post2swellRT(session,wave_id,tags):
    #Making the Update Link
    update_link = swellrt + 'object/' + wave_id + '/tags'
    
    try:
        update = session.post(update_link, json=tags)
    except requests.exceptions.RequestException as e:
        app.logger.info('Updating to SwellRT failed')


if __name__ == "__main__":

    #Building dictionary from NLTK Corpus
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))

    #Initialising mytagger object which tags the string
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))

    #Webserver running in debug mode to show logs
    app.run(debug=True, host='0.0.0.0')
