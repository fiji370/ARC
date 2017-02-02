from nltk import *
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.collocations import *

with open('Omnilingual.txt') as text:
    sci1 = text.read()

with open('The House on the Borderland.txt') as text:
    sci2 = text.read()

with open('WoTW.txt') as text:
    sci3 = text.read()

with open('Star Surgeon.txt') as text:
    sci4 = text.read()

with open('The Illustrated Man.txt') as text:
    sci5 = text.read()

with open('Oz.txt') as text:
    fan1 = text.read()

with open('Robin Hood.txt') as text:
    fan2 = text.read()

with open('King Arthur.txt') as text:
    fan3 = text.read()

with open('The Mysterious Affair at Styles.txt') as text:
    mys1 = text.read()

with open('The Sign of the Four.txt') as text:
    mys2 = text.read()

with open('The Hound of the Baskervilles.txt') as text:
    mys3 = text.read()

with open('INPUT.txt') as text:
    INPUT = text.read()
    
question = raw_input("Question: \n")

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures

def interpret(text, doc):
    verbList = ["VB", "VBP", "VBD", "VBG", "VBN", "VBZ"]
    contextList = []
    verbs = []
    nouns = []
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    doc = doc.lower()
    docSent = sent_tokenize(doc)
    doc = word_tokenize(doc)
    doc = [i for i in doc if i not in punct]
    doc = [i for i in doc if i not in stop_words]
    text = text.lower()
    text = word_tokenize(text)
    text = [i for i in text if i not in punct]
    text = [i for i in text if i not in stop_words]
    posTagged = pos_tag(text)
    chunked = ne_chunk(posTagged, binary=True)
    for i in chunked:
        if i[1] == 'NN':
            nouns.append(i[0])
        if i[1] in verbList:
            verbs.append(i[0])
    for i in doc:
        for x in range(len(nouns)):
            if i in nouns[x]:
                contextList.append(nouns[x])
            for b in range(len(contextList)):
                if contextList[b] in nouns[x]:
                    contextList[b] = nouns[x]
                    
    return contextList

def clean_up(doc):
    stop = set(stopwords.words('english'))
    doc = doc.lower()
    doc = word_tokenize(doc)
    doc = [i for i in doc if i not in stop]
    return dict([(word, True) for word in doc])

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools, nltk, string
    
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]

    return set([cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)])

labeled = ([(words, 'sci fi') for words in sent_tokenize(sci1)] +
           [(words, 'sci fi') for words in sent_tokenize(sci2)] +
           [(words, 'sci fi') for words in sent_tokenize(sci3)] +
           [(words, 'sci fi') for words in sent_tokenize(sci4)] +
           [(words, 'sci fi') for words in sent_tokenize(sci5)] +
           [(words, 'mystery') for words in sent_tokenize(mys1)] +
           [(words, 'mystery') for words in sent_tokenize(mys2)] +
           [(words, 'mystery') for words in sent_tokenize(mys3)] +
           [(words, 'fantasy') for words in sent_tokenize(fan1)] +
           [(words, 'fantasy') for words in sent_tokenize(fan2)] +
           [(words, 'fantasy') for words in sent_tokenize(fan3)])

import random
random.shuffle(labeled)

featuresets = [(clean_up(n), which) for (n, which) in labeled]

classifier = nltk.NaiveBayesClassifier.train(featuresets)

print classifier.classify(clean_up(INPUT))

dist = classifier.prob_classify(clean_up(INPUT))
for label in dist.samples():
    print("%s: %f" % (label, dist.prob(label)))

print interpret(question, INPUT)
