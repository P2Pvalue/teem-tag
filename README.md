#teem-tag

##Objective

Automatic anaysis of the description of teams in Teem to get valid and important tokens.

##Documentation

* reader splits on whitespaces, punctuation etc. Also information like proper nouns and terminal words are recorded.
* stemmer reduces the words to root words. eg working and worked become work so they don't appear twice.
* rater rates them based on normalized weights. Default weights normalized from nltk.corpus.reuters.

