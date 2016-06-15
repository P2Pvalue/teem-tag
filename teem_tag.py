#!/usr/bin/env python
# -*- coding: utf-8 -*-


from tagger import *
from pymongo import *
from extras import build_dict_from_nltk
import os, pickle, pymongo

from bson.objectid import ObjectId 


if __name__ == '__main__':

    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')

    weights = pickle.load(open('data/nltkdict.pkl'))
    mytagger = Tagger(Reader(), Stemmer(), Rater(weights))
    
    # string = "The P2Pvalue project is mapping the diffusion and hybridization of peer production and investigating the conditions which favour collaborative creation and the logic of value of these emerging forms."
    # tags = mytagger(string, 5)

    client = MongoClient('mongodb://172.17.0.2:27017/')
    collection = client.wiab.models
    
    cursor = collection.find()
    key = "description"

    for doc in cursor:
        root = doc['root']
        if key in root:
            print mytagger(root[key],5) 