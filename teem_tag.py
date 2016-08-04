#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
from flask import Flask, request
import os, pickle, pymongo
import json

# Intialising Flask. It acts as webserver so that it catch any POST request that contains the text that one wants to tag 
app = Flask(__name__)

#Listening on http://0.0.0.0:5000
@app.route("/", methods=['GET', 'POST'])
def tags():
    if request.method == 'POST':
        data = request.get_json()
        tags = mytagger(data['data']['text'],10)
        return json.dumps(tags, default=lambda x: str(x).strip('"\''))
    else
        return "Hello from Teem-tag"

if __name__ == "__main__":

    #Building dictionary from NLTK Corpus
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))

    #Intialising mytagger object which tags the string
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))

    #Webserver running in debug mode to show logs
    app.run(debug=True, host='0.0.0.0')
