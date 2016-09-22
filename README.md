#SwellRT Contest Submission Module
Module which interacts with SwellRT, a project under [P2PValue Project](https://p2pvalue.eu/). 

##Objective
We are targeting how to improve SwellRT externally. Our idea is devised from the patterns we observed:
* Since most consumers of SwellRT are normal people, mainly web developers who want to use these applications to reduce their work, so they necessarily won't have the money or the infrastructure or the skills to incorporate machine learning or image processing or natural language.
* The above mentioned technologies and computer sciences are in a lot of demand. These emerging sciences have made new insights which were not possible 5 years back.

So there is this gap or friction between these 2 points. We are trying to create an ecosystem of apps that strengthen the resolve of SwellRT and make it a dominating technology in the field of BaaS. 

## Usecases:
* You want a image processing support. Use an app from the ML+NLP ecosytem of SwellRT. 
* You want a data science library -> okay done, ping the similar API. Though our idea is very small,  this can become a huge opening for developers writing apps for SwellRT. As SwellRT talks about decentralizing, we take it in a very literal way: of decentralizing the skills only available to the privileged people and hand it over to the masses. 

## Inspiration:
This is how ownCloud became a giant force in open source community since it had a app driven approach. We both are a part of the organization and we felt that the value proposition of the product was okay, but the engagement model in terms of developers and the community using it was high. 

## What have we done till now:
We have built upon teem-tag module which Prastut had developed under the Google Summer of Code program. We have primarily added 2 new features for now:
* NLP (click on the links to view code)
 * [Text summarization.](https://github.com/P2Pvalue/teem-tag/blob/swellrt-contest/teem_tag.py#L52-L55)
 * [Text tagging.](https://github.com/P2Pvalue/teem-tag/blob/swellrt-contest/teem_tag.py#L49-L50)
* [Image processing through TensorFlow.](https://github.com/P2Pvalue/teem-tag/blob/swellrt-contest/teem_tag.py#L79-L81)


## Architecture
This module heavily uses nltk package for most of it's NLP tasks as well as Tensorflow for image processing and convulutional neural network support. It's build on top of Flask to provide a webserver. The module integrates as a docker container with [SwellRT](http://swellrt.org/), the full-stack backend framework for Teem. Following is a schematic diagram for the same:
![alt tag](https://cloud.githubusercontent.com/assets/10279686/17645910/ab396276-61d0-11e6-8553-2cf8984c5c96.png)

## Project Setup

#### Installing required dependencies

```pip install -r /path/to/requirements.txt```

#### Tensor flow setup

##### Ubuntu:
```
sudo apt-get install python-pip python-dev
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl
sudo pip install --upgrade $TF_BINARY_URL
```
##### Mac OS X
```
sudo easy_install pip
sudo easy_install --upgrade six
export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.10.0-py2-none-any.whl
sudo pip install --upgrade $TF_BINARY_URL
```

## Contributors

* [Fenil Patel](https://github.com/patelfenil)
* [Prastut Kumar](https://github.com/prastut/)
