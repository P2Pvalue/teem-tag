#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import tagger
from textteaser import TextTeaser
from pymongo import *
from flask import Flask, request
from urlparse import urljoin
import os, sys, pickle, pymongo, json, requests, logging
from flask.views import View
from flask import Flask
from flask import render_template, redirect
from werkzeug import secure_filename

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
        app.logger.info(data)
        #Initialisation for context
        wave_id = data['waveid']
        description = data['data']['text']
        name = data['data']['name']

        #Generating tags
        tags = json.dumps(mytagger(data['data']['text'],10), default=lambda x: str(x).strip('"\''))

        #Generating summary of 4 lines
        tt = TextTeaser()
        sentences = tt.summarize(name, description)
        summary = json.dumps(sentences[:4])

        
       
        #For logs
        app.logger.info(tags)
        app.logger.info(summary);
        
        post2swellRT(session,wave_id,tags,summary)
        
        return json.dumps(True)
    else:
        tags = json.dumps("Hello from Teem Tag",10, default=lambda x: str(x).strip('"\''))
        return tags


@app.route("/image_classify", methods=['GET', 'POST'])
def classify_image():
     return render_template('image.html')
        
@app.route('/imageupload/', methods=['POST'])
def imageupload():
    image=request.form['path']
    #image = "/home/fenil/Pictures/img1.jpg"
    sys.path.append("tensorflow/models/image/imagenet")
    import classify_image

    image_classification = classify_image.run_inference_on_image(image)
    #app.logger.info(image_classification)
    return render_template('image.html', image_classification=image_classification,image=image)


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


def post2swellRT(session,wave_id,tags,summary):
    #Making the Update Link for tags
    update_link = swellrt + 'object/' + wave_id + '/tags'
    
    try:
        update = session.post(update_link, json=tags)
    except requests.exceptions.RequestException as e:
        app.logger.info('Updating tags to SwellRT failed')

    #Making the Update Link for summary
    summary_update_link = swellrt + 'object/' + wave_id + '/summary'
    
    try:
        update = session.post(summary_update_link, json=summary)
    except requests.exceptions.RequestException as e:
        app.logger.info('Updating summary to SwellRT failed')


if __name__ == "__main__":

    #Building dictionary from NLTK Corpus
    if not(os.path.isfile('data/nltkdict.pkl')):
        build_dict_from_nltk('data/nltkdict.pkl')
    
    weights = pickle.load(open('data/nltkdict.pkl'))

    #Initialising mytagger object which tags the string
    mytagger = tagger.Tagger(tagger.Reader(), tagger.Stemmer(), tagger.Rater(weights))

    #Webserver running in debug mode to show logs
    app.run(debug=True, host='0.0.0.0')
