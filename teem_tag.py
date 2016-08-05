#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
from flask import Flask, request
from urlparse import urljoin
import os, pickle, pymongo, json, requests

# Initialising Flask. It acts as webserver so that it catch any POST request that contains the text that one wants to tag 
app = Flask(__name__)
swellrt = 'http://0.0.0.0:9898/swell/'

session = False

#Listening on http://0.0.0.0:5000
@app.route("/", methods=['GET', 'POST'])
def tags():

    global session
    
    if not session:
        session = authfromSwellRT()

    if request.method == 'POST':
        data = request.get_json()
        print data
        
            #Initialisation
        wave_id = data['waveid']
        description = data['data']['text']

        tags = json.dumps(mytagger(data['data']['text'],10), default=lambda x: str(x).strip('"\''))
        hello = post2swellRT(session,wave_id,tags)
        
        #For logs
        print tags
        print "POST2SWELLRT"
        print hello

        return json.dumps(True)
    else:
        tags = json.dumps(mytagger("Hello from the other side",10), default=lambda x: str(x).strip('"\''))
    
        return tags



def authfromSwellRT():
    session = requests.session()
    swellrt_auth_link = urljoin(swellrt,'auth')
    session.post(swellrt_auth_link, json={"id":"teemtag@local.net","password":"teemtag"})
    auth_test = session.get(swellrt_auth_link)
    if auth_test.status_code == 200:
        return session
    else:
        return False


def post2swellRT(session,wave_id,tags):
    update_link = swellrt + 'object/' +wave_id + '/tags'
    print update_link
    update = session.post(update_link, json=tags)
    print update.content
    return update

if __name__ == "__main__":

    #Building dictionary from NLTK Corpus
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))

    #Intialising mytagger object which tags the string
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))

    #Webserver running in debug mode to show logs
    app.run(debug=True, host='0.0.0.0')
