### WELCOME TO MY PROGRAM, READ THIS FIRST PLEASE ###

"""Welcome, the red text lines are "comments", these are your guides to interpreting
this nonsense. Anyways, READ THIS OVER CAREFULLY. I really don't want to have to
answer stupid questions. Please, to the best of your abilities, try to understand what
I have written. I have tried my best to make it as simple as possible for the normal
person, but there is always room for someone not understanding. Please do not ask me for
specifics on how certain sections work, I can't really explain it much more in-depth than what
I have written. Also, any sections that I have commented saying things like "legacy" or "you don't
need to know this" or "I don't use this" AREN'T RELAVENT TO THE PROGRAM. I WILL NOT TAKE QUESTIONS
ON THESE. Finally, if you have any concerns regarding how the program works, I am happy to take
suggestions, but also acknowledge that I REALLY know how this program and library works, so don't
always expect me to respond to them. I think that's pretty much it. Have fun."""

### END OF INTRO ###


# This just imports all the essential libraries for the project, NLTK is the language processing
# library. grammar_check and string may be retired, but I don't remember so I'm keeping them for legacy

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

# Load literature into string variables (just normal program text)

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
    
# This is special, this reads the input text
with open('INPUT.txt') as text:
    INPUT = text.read()

# This just grabs whatever the question is and saves it as the variable "question".
question = raw_input("Question: \n")

# These are just legacy things for experiments I was doing on bigrams, they aren't used anymore...
# they are usually used in the process of getting pairs or fews of words.
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures

# This is a function. A function is a series of steps. Def just declares it as a function. Text and doc
# are whatever is entered when the function is used. Scroll down to red text that says "HERE" for an example of using a function.
def interpret(text, doc):
    
# This line here gets a list of words from NLTK called "stopwords". Stopwords are words that mean nothing
# and are not useful at all for language processing
    stop = set(stopwords.words('english'))
    
# This line declares a list named "merged" (declare means to tell the program to make it.) Right now
# the list is empty
    merged = []
    
# Declares a list named "nouns"
    nouns = []
    
# Declares a list named "replacements"... I'm actually not sure if I still use this
    replacements = []
    
# Declares a list "matchedSim". This list contains sentences with nouns that are close to the nouns
# in the question
    matchedSim = []
    
# This line here tells the program to take "doc" (doc is the text from the "INPUT" file),
# which was given to the function, and splits it
# into sentences, then saves it to a variable named "docSents"
    docSents = sent_tokenize(doc)

# This line takes "text" (text is whatever the question to be interpreted is), and removes all the stop words
# from it
    stopped = [i for i in word_tokenize(text) if i not in stop]
    
# This is where things start to get tricky... First of all, pos_tag takes each word, and puts it in
# a list beside its part of speech. ne_chunk takes those words and parts of speech, and checks for people
# or things. The reason I'm not just using something that simply finds nouns, is because "True Son", for example
# would be split into two.

# Anyways, "for" means take a chunk. "try" means if there is an error, go to "except". "except" tells
# it to continue the loop. "nouns.append(i.leaves())" means take the "leaves" ("True", "Son") out
# of a person or thing "tree", and add them to the list of nouns.
# So now nouns would have an entry "True Son", for example

# In all, this means: for every chunk in the question, check if it is a person or thing... If it is
# then add all of it to nouns.
    for i in ne_chunk(pos_tag(stopped)):
        try:
            nouns.append(i.leaves())
        except:
            continue
        
# This is essentially the same thing, except it gets things like "father" that aren't really specific
# people or things. These are also added to nouns.
    for i in pos_tag(stopped):
        if i[0] in nouns:
            continue
        if "NN" in i[1]:
            nouns.append([i])
            
# This just removes all the extra part of speech and person thing stuff, and just leaves the actual words
# like "Bilbo" for example
    nouns = [x[0] for i in nouns for x in i]
    
# These two lines just take any entries that are identical for some reason, and removes them.
    nouns = set(nouns)
    nouns = list(nouns)
    
# "secNouns" means secondary nouns. This line makes a list with all of the nouns that appear less than
# 50 times in the input text. Secondary nouns are important, because they are unique; making it easier
# to find relavent sentences. We wouldn't want everything close to "Bilbo" in The Hobbit now would we?
    secNouns = [i for i in nouns if word_tokenize(doc).count(i) < 50]
    
# I thought about extracting verbs, and soon realized they are useless for finding anything. Verbs
# are rarely used twice. Legacy
    verbs = [i[0] for i in pos_tag(stopped) if "VB" in i[1]]
    
# This line takes all of the sentences in the input doc, and sees if secondary nouns are in them, if so:
# add them to "matched"
    matched = [i for i in docSents for x in word_tokenize(i)
               if x in secNouns]
    
# This was just for sentence numbers, I was trying to narrow things down with these... It doesn't really
# work that well. Legacy
    matchedSimSentNums = []
    
# Same thing, just grabs the number of sentences. Legacy
    matchedSentNums = [docSents.index(i) for i in docSents for x in word_tokenize(i) if x in secNouns]
    
# This line takes all of the previously matched sentences (y'know, the ones with secondary nouns in them.)
# and finds other nouns in the matched sentences. "NN" is the code for noun (you may have guessed this already)
    similar = [x[0] for i in matched for x in pos_tag(word_tokenize(i)) if "NN" in x[1]]
    
# This takes all the nouns in all the matched sentences, and grabs only ones that appear less than 5 times
# in the entire doc. Uniqueness is our friend.
    similar = [i for i in similar if word_tokenize(doc).count(i) < 5]
    
# Legacy... Please don't question these, they aren't important, and I'm not leaving out information.
# You don't need to know, this isn't used anymore, and that's that.
# Lol this is only because I can't remember what "count" was for, and I knew that you were going to ask
# if I didn't explain thoroughly
    count = 0
    
# You've seen this before... It simply removes duplicates
    similar = set(similar)
    similar = list(similar)
    
# Ooh... Now on to the big boy stuff. This is kinda complicated; basically, it matches any sentences with
# similar nouns, and original question nouns. It also checks if the sentence behind the current sentence has
# any of the similar or original nouns, or even the sentence in front of the current sentence.
# Please don't try to understand this, or even ask questions about it. I'm willing to bet that even
# the most skilled Python programmers find this disgusting and illegible.
    for i in docSents:
       for x in word_tokenize(i):
          if x in secNouns or x in similar:
             matchedSim.append(i)
             matchedSimSentNums.append(docSents.index(i))
          try:
              for c in word_tokenize(docSents[docSents.index(i) - 1]):
                 if c in secNouns:
                    matchedSim.append(i)
                    matchedSimSentNums.append(docSents.index(i))
              for c in word_tokenize(docSents[docSents.index(i) + 1]):
                 if c in secNouns:
                    matchedSim.append(i)
                    matchedSimSentNums.append(docSents.index(i))
          except:
              continue
            
    
# This takes both sentences with original nouns, and similar nouns, and all the extra stuff we got with
# that big mess of code above, and adds it to a big list that we declared earlier, "merged".
    for i in matchedSim:
        merged.append(i)
    for i in matched:
        merged.append(i)
        
# My brain is at a point where it hurts... This line finds all of the nouns in merged and adds them to
# a list.
    matchedMerged = [x[0] for i in merged for x in pos_tag(word_tokenize(i)) if "NN" in x[1]]
    
# This (it should be obvious at this point) removes duplicates
    merged = set(merged)
    merged = list(merged)
    
# declares some lists
    newMerged = []
    newNewMerged = []
    
# This here basically tells the computer to take all the nouns in all of the merged sentences, and then
# find the ratio of extracted nouns to nouns that aren't related.
# If there is a high density of nouns that we know and have extracted, then we keep that sentence, as well
# as the ones before and after it. Idk, it works, and gets anything that may have fallen through the cracks
# that could be relevant.
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
                        if ratio > 0.74:
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
                        
# This does it again with the new sentences, but essentially makes sure that the sentences we added above
# (the ones we added before or after the actual matching one) are relevant.
    for i in range(len(newMerged)):
        nums1 = []
        matchedMerged1 = []
        for x in pos_tag(word_tokenize(newMerged[i])):
            if "NN" in x[1]:
                matchedMerged1.append(x[0])
                for x in matchedMerged1:
                    if x in similar or x in secNouns:
                        nums.append(matchedMerged1.count(x))
                        numsT = sum(nums)
                        ratio = float(numsT) / float(len(matchedMerged1))
                        if ratio > .74:
                            newNewMerged.append(newMerged[i])
                        else:
                            continue
                        
# Again, removing duplicates
    newNewMerged = set(newNewMerged)
    newNewMerged = list(newNewMerged)
    newNewNewMerged = []
    for i in newNewMerged:
        points = []
        for x in word_tokenize(i):
            if x in secNouns:
                points.append(3)
            elif x in similar:
                points.append(2)
            else:
                points.append(1)
        points = max(points)
        if points > 2:
            newNewNewMerged.append((i, points))
        if points == 2:
            newNewNewMerged.append((i, points))
        if points < 2:
            newNewNewMerged.append((i, points))
            
    newNewNewMerged.sort(key=lambda x: x[1])
    newNewNewMerged = [i for i in reversed(newNewNewMerged)]
    newNewNewMerged = [i[0] for i in newNewNewMerged]
    newNewNewMerged = [i for i in newNewNewMerged if len(word_tokenize(i)) > 5]
# "\n" means "new line". This line of code takes all of the sentences, joins them together into a string, and seperates them
# by one line of blank space. The reason there are two "\n"'s is because one just puts it on a new line directly under, and the
# other makes a space.
    final = "\n\n".join(newNewNewMerged[0:5])
    
# Welcome to the end of the function! This line returns the relevant sentences that have been formatted above to whatever asked for them.
    return final

# This is just for genre classification, this just finds the popular words and returns them. It is what formats the datasets for machine learning
def clean_up(doc):
    stop = set(stopwords.words('english'))
    doc = doc.lower()
    doc = word_tokenize(doc)
    doc = [i for i in doc if i not in stop]
    return dict([(word, True) for word in doc])

# This doesn't matter, I stole it from a site to play with it for noun phrase chunking (extracting basic sentences with nouns and verbs in them).
# I don't even think it's used for anything in the program at this point. The double hastags (##) below mean I didn't write those comments. They
# were actually from the person I stole it from.
# Also, I know you're going to bring this up... Don't worry, this code will not be in the final version. I'm not using it, and all the code that is
# actually used is mine
def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools, nltk, string
    
    ## exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    ## tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    ## join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]

    return set([cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)])

# This part here takes all of the training literature and labels the words in the sentences with their genre
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

# This shuffles the list so that the computer isn't biased, and gets training in a different order every time.
# You may want to ask about this too... To be honest, I don't know exactly why I need to do this part, the NLTK book
# says I have to though.
import random
random.shuffle(labeled)

# This just grabs the important features from the training data
featuresets = [(clean_up(n), which) for (n, which) in labeled]

# This just trains a classifier with our nice, clean, labeled data
classifier = nltk.NaiveBayesClassifier.train(featuresets)

# This prints which genre the computer thinks the input text is.
print classifier.classify(clean_up(INPUT)) + "\n"


# HERE
# This is where the interpret function is called. With our saved input question, and our input text.
# It then prints whatever interpret returned
print interpret(question, INPUT)

### Hey, you've reached the end of the document. Congratulations, I hope you understood. If you didn't, time to read it again. ###
