#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from pymongo import *
import os, pickle, pymongo

from bson.objectid import ObjectId 

#Configure database link
db_host = os.environ.get('MONGO_PORT_27017_TCP_ADDR')
db_port = os.environ.get('MONGO_PORT_27017_TCP_PORT')



if __name__ == '__main__':

    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')

    
    weights = pickle.load(open('data/nltkdict.pkl'))
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))
    
    string = "The P2Pvalue project is mapping the diffusion and hybridization of peer production and investigating the conditions which favour collaborative creation and the logic of value of these emerging forms."
    tags = mytagger(string, 5)

    print tags

    client = MongoClient(db_host,int(db_port))
    collection = client.wiab.models
    
    cursor = collection.find()
    key = "description"

    for doc in cursor:
        print doc