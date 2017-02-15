from nltk import *
import nltk
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.collocations import *
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string
import grammar_check
from nltk.corpus import wordnet as wn

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




def interpret(text, doc):
    
    ## Declare some lists for later use, probably temporary storage, as well as lists of important words.
    stop = set(stopwords.words('english'))
    
    merged = []

    nouns = []

    replacements = []

    matchedSim = []
    
    docSents = sent_tokenize(doc)
    
    
    
    ## Declare a list of unimportant "stopwords."
    stopped = [i for i in word_tokenize(text) if i not in stop]


    ## This just grabs named entities from the "stopped" input question
    for i in ne_chunk(pos_tag(stopped)):
        try:
            nouns.append(i.leaves())
        except:
            continue
       
    ## This just formats the named entites so that they're all together properly
    nouns1 = []
    for i in nouns:
        transientList = []
        for x in i:
            transientList.append(x[0])
        nouns1.append(transientList)
    nouns1 = [" ".join(i) for i in nouns1]
    
    ## Get other nouns, format nouns list.
    nouns = nouns1
    for i in pos_tag(stopped):
        if "NN" in i[1] and i[0] not in nouns:
            nouns.append(i[0])  
    nouns = set(nouns)
    nouns = list(nouns)

    ## "Secondary" nouns. This gets the nouns that are used less, but are still relevant.
    secNouns = [i for i in nouns if word_tokenize(doc).count(i) < 50 and word_tokenize(doc).count(i) > 1]
    ## Getting verbs, it's probably important.
    verbs = [i[0] for i in pos_tag(stopped) if "VB" in i[1]]
    
    ## Match sentences with secNouns in them.
    matched = [i for i in docSents for x in word_tokenize(i)
               if x in secNouns]
    
    ## Declare the list "similar", this gets named entities other than the matched ones in the sentences
    similar = []
    
    
    
    for i in matched:
        for x in ne_chunk(pos_tag(word_tokenize(i))):
            try:
                similar.append(x.leaves())
            except:
                continue
            
    ## Formatting the named entities again, but for similar.
    similar1 = []
    for i in similar:
        transientList = []
        for x in i:
            transientList.append(x[0])
        similar1.append(transientList)
    similar1 = [" ".join(i) for i in similar1]
    similar = similar1



    ## This gets similar nouns that aren't named entities.
    for i in matched:
        for x in pos_tag(word_tokenize(i)):
            if "NN" in x[1] and x[0] not in similar:
                similar.append(x[0])
    ## This just gets the good, unique, pertinent similar nouns.
    similar = [i for i in similar if word_tokenize(doc).count(i) < 24 and word_tokenize(doc).count(i) > 1]
    similar = set(similar)
    similar = list(similar)
    
    ## This rematches all sentences with secNouns or similar, and also gets the sentences in front and behind.
    for i in docSents:
       for x in word_tokenize(i):
          if x in secNouns or x in similar:
             matchedSim.append(i)
          try:
              for c in word_tokenize(docSents[docSents.index(i) - 1]):
                 if c in secNouns:
                    matchedSim.append(i)
              for c in word_tokenize(docSents[docSents.index(i) + 1]):
                 if c in secNouns:
                    matchedSim.append(i)
          except:
              continue
    
    
           
    for i in matchedSim:
        merged.append(i)
    for i in matched:
        merged.append(i)
    
    ## This seems redundant, but it isn't, it just gets nouns again for some ratios.
    
    matchedMerged = [x[0] for i in merged for x in pos_tag(word_tokenize(i)) if "NN" in x[1]]
    
    merged = set(merged)
    merged = list(merged)
    
    newMerged = []
    newNewMerged = []
    
    ## This gets all the relevant nouns, and divides them by irrelevant nouns.
    for i in range(len(merged)):
        nums = []
        matchedMerged = []
        for x in pos_tag(word_tokenize(merged[i])):
            if "NN" in x[1]:
                matchedMerged.append(x[0])
                for x in matchedMerged:
                    if x in similar or x in secNouns:
                        nums.append(matchedMerged.count(x))
                        numsT = sum(nums)
                        ratio = float(numsT) / float(len(matchedMerged))
                        if ratio > 0.5:
                            try:
                                newMerged.append(merged[i - 1])
                            except:
                                pass
                            newMerged.append(merged[i])
                            try:
                                newMerged.append(merged[i + 1])
                            except:
                                pass
                        else:
                            continue               
    ## I kept this because I didn't want to refactor anything, because there used to be another step.
    doubleNewMerged = []
    newNewMerged = set(newMerged)
    newNewMerged = list(newMerged)
    newNewNewMerged = []
    
    
    ## This scores the sentences based on how many relevant nouns they have in them. 
    for i in newNewMerged:
        points = []
        for x in word_tokenize(i):
            if x in secNouns:
                points.append(3)
            elif x in similar:
                points.append(2)
            else:
                points.append(1)
        points = sum(points)
        newNewNewMerged.append((i, points))
    newNewNewMerged.sort(key=lambda x: x[1])
    newNewNewMerged = [i for i in reversed(newNewNewMerged)]
    newNewNewMerged = [i[0] for i in newNewNewMerged if len(word_tokenize(i[0])) > 10]
    
    newNewNewMerged = set(newNewNewMerged)
    newNewNewMerged = list(newNewNewMerged)
    
    ## This gets a snippet containing the actual sentences, including those behind and after it.
    for i in newNewNewMerged:
        transientList = []
        try:
            transientList.append(docSents[docSents.index(i) - 2])
        except:
            pass
        try:
            transientList.append(docSents[docSents.index(i)])
        except:
            pass
        try:
            transientList.append(docSents[docSents.index(i) + 2])
        except:
            pass
        doubleNewMerged.append(" ".join(transientList))
        continue
    
    ## Delcare a whole bunch of lists for the operations that we're doing.
    proNouns = []
    nounsNouns = []
    lenNouns = []
    lenNounsMore = []
    ration = []
    tripleNewMerged = []
    answer = []
    
    ## This gets the pronouns in the snippets.
    for i in doubleNewMerged:
        transientList = []
        for x in pos_tag(word_tokenize(i)):
            if "PRP" in x[1]:
                transientList.append(x[0])
        proNouns.append(transientList)
        
        
    ## This gets the nouns in the snippets.
    for i in doubleNewMerged:
        transientList = []
        for x in pos_tag(word_tokenize(i)):
            if "NN" in x[1]:
                transientList.append(x[0])
        nounsNouns.append(transientList)
        
        
    ## This gets the length of the pronouns, as well as nouns.
    for i in proNouns:
        lenNouns.append(len(i))
    for i in nounsNouns:
        lenNounsMore.append(len(i))

    ## This gets the ratio of pronouns to nouns, and ranks sentences based on their ratio.
    for i in range(len(lenNouns)):
        ration = float(lenNouns[i]) / float(lenNounsMore[i]) / float(len(doubleNewMerged[i]))
        if ration < 0.005:
            tripleNewMerged.append((doubleNewMerged[i], ration))
        else:
            continue
    rations = [i[1] for i in tripleNewMerged]
    ## This just formats the list
    tripleNewMerged.sort(key=lambda x: x[1])
    tripleNewMerged = [i for i in newNewNewMerged]

    print str(nouns) + " <--- NOUNS\n"
    
    print str(rations) + " <--- RATIO OF PRONOUNS TO NOUNS\n"
    
    print str(lenNouns) + " <--- LEGNTH OF PRONOUNS\n"
    
    print str(lenNounsMore) + " <--- LENGTH OF NOUNS\n"
    
    print str(secNouns) + " <--- SECONDARY NOUNS\n"

    print str(similar) + " <--- SIMILAR NOUNS\n"
    
    ## This formats all the snippets into one text block (with the appropriate newlines.)
    
    final = "\n\n".join(tripleNewMerged)
    
    return final


## Clean up any input for classification.
def clean_up(doc):
    stop = set(stopwords.words('english'))
    doc = doc.lower()
    doc = word_tokenize(doc)
    doc = [i for i in doc if i not in stop]
    return dict([(word, True) for word in doc])

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


## Print classification, along with the question answers.
print classifier.classify(clean_up(INPUT)) + "\n"

print interpret(question, INPUT)