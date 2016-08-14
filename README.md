#teem-tag
Module which interacts with the [Teem](https://teem.works/), a project under [P2PValue Project](https://p2pvalue.eu/). 

Made with <3 for open-source. This module is part of the matchmaking proposal for which I got selected as a [Google Summer of Code Student](https://summerofcode.withgoogle.com/projects/#5751555160539136) in 2016, under the organization [Berkman Klein Center for Internet & Society](https://cyber.law.harvard.edu/). 

Additional Links: 
* [Matchmaking Proposal](https://docs.google.com/document/d/1DwtxhYupN_e8bX13vntU7csiP4hrbZq4MftBJGhE6v0/edit?usp=sharing) for GSoC.
* [Pycon Delhi 2016 Slides](https://in.pycon.org/cfp/2016/proposals/building-an-automatic-keyphrase-extraction-system-using-nltk-in-python~e9g4b/)

##Objective

Automatic analysis of the description of teams in Teem to get valid and important tokens. Currently new users have a lot of friction in finding communities of their interest. By analysing the data from the communities, we can generate a map of interests. These interests can therefore be grouped and the user can be onboarded more easily through the idea of having to select their interests and then being directed to relevant communities. Future goals of this module to become a full fletched module for ML + NLP tasks related to the project. 

##Architecture
This module heavily uses nltk package for most of it's inner working. It's build on top of Flask to provide a webserver. The module integrates as a docker container with [SwellRT](http://swellrt.org/), the full-stack backend framework for Teem. Following is a schematic diagram for the same:
![alt tag](https://cloud.githubusercontent.com/assets/10279686/17645910/ab396276-61d0-11e6-8553-2cf8984c5c96.png)

##Brief Explanation
Extracting tags from a text document involves at least three steps: 
* Splitting the document into words. (Reading)
* Grouping together variants of the same word. (Stemming) 
* Ranking them according to their relevance. (Ranking)

###Reader
A Reader object accepts a input string (document), perform normalisation and noise filteringof the text (such as turning everything into lower case), analyse the structure of the phrases and punctuation, and return a list of words respecting the order in the text, with some additional information such as which ones look like proper nouns, or are at the end of a phrase. 

###Stemmer
The Stemmer tries to recognise the root of a word, in order to identify slightly different forms. This is already a quite complicated task, and it's clearly language-specific. The stem module in the NLTK package provides algorithms for many languages. Currently the module only supports English language and uses PorterStemmer as the default stemmer. 

###Rater
The Rater takes the list of words contained in the document, together with any additional information gathered at the previous stages, and returns a list of tags (i.e. words or small units of text) ordered by some idea of "relevance".
It turns out that just working on the information contained in the document itself is not enough, because it says nothing about the frequency of a term in the language. For this reason, the module consists of analysing a corpus (i.e. a sample of documents written in the same language) to build a dictionary of known words. This is taken care by the build_dict() function. It is advised to build your own dictionaries, and the build_dict_from_nltk() function in the [build_dict.py](https://github.com/P2Pvalue/teem-tag/blob/master/core/build_dict.py) enables you to use the corpora included in NLTK.
