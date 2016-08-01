#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
from flask import Flask
import os, pickle, pymongo
import json


from bson.objectid import ObjectId 

#Configure database link
db_host = os.environ.get('MONGO_PORT_27017_TCP_ADDR')
db_port = os.environ.get('MONGO_PORT_27017_TCP_PORT')

app = Flask(__name__)

@app.route("/")
def tags():
    string = "The P2Pvalue project is mapping the diffusion and hybridization of peer production and investigating the conditions which favour collaborative creation and the logic of value of these emerging forms."
    data = { 'data' : mytagger(string,5)}
    return json.dumps(data, default=lambda x: str(x).strip('"\''))
    

if __name__ == "__main__":
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))
    
    # client = MongoClient('172.17.0.2',27017)
    # collection = client.swellrt.models
    # for doc in cursor:
    #     root = doc['root']
    #     if key in root:
    #         data = {'waveid' : doc['wave_id'],  'waveletid' : doc['wavelet_id'], 'path' : 'xyz', 'data' : mytagger(root[key],10)}
    #         print json.dumps(data, default=lambda x: str(x).strip('"\''))

    
    # cursor = collection.find()
    # key = "description"

    app.run(debug=True, host='0.0.0.0')



    