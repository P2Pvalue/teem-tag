#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
from flask import Flask, request
from urlparse import urljoin
import os, sys, pickle, pymongo, json, requests

# Initialising Flask. Webserver to handle POST from SwellRT. 
app = Flask(__name__)
# SwellRT IP. Works only with docker-compose setup.
swellrt = 'http://swellrt:9898/swell/'

session = False

# For authentication, defaults to username = teemtag, password
tag_user = os.environ.get('TEEMTAG_USERNAME')
tag_pwd = os.environ.get('TEEMTAG_PASSWORD')

@app.route("/", methods=['GET', 'POST'])
def tags():

    global session
    

    if request.method == 'POST':

        if not session:
            session = authfromSwellRT()

        data = request.get_json()
        
        #Initialisation
        wave_id = data['waveid']
        description = data['data']['text']

        tags = json.dumps(mytagger(data['data']['text'],10), default=lambda x: str(x).strip('"\''))
       
        #For logs
        print tags
        
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
            session.post(swellrt_auth_link, json={"id": tag_user + "@local.net","password": tag_pwd})
        else:
            session.post(swellrt_auth_link, json={"id":"teemtag@local.net","password":"teemtag"})
    except requests.exceptions.RequestException as e:    
        print 'Authentication failed'
        print e
        sys.exit(1)

    try:
        auth_test = session.get(swellrt_auth_link)
    except requests.exceptions.RequestException as e:    
        print 'Authentication checking failed'
        print e
        sys.exit(1)
    
    if auth_test.status_code == 200:
        return session
    else:
        print 'Cannot authenticate from SwellRT. Exiting!'
        sys.exit(1)


def post2swellRT(session,wave_id,tags):
    #Making the Update Link
    update_link = swellrt + 'object/' + wave_id + '/tags'
    try:
        update = session.post(update_link, json=tags)
    except requests.exceptions.RequestException as e:
        print 'Updating to SwellRT failed'
        print e

if __name__ == "__main__":

    #Building dictionary from NLTK Corpus
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))

    #Initialising mytagger object which tags the string
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))

    #Webserver running in debug mode to show logs
    app.run(debug=True, host='0.0.0.0')
