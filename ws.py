import nltk
from nltk.corpus import wordnet as wn
import ssl
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#nltk.download('wordnet') #only need to do this once
#nltk.download("punkt") #need to do this the first time you run it
#nltk.download('stopwords')

#nltk.download('wordnet')
def compute_overlap(set1, set2):
    count_overlap = 0
    for item in set1:
        if item in set2:
            count_overlap += 1
    return count_overlap
def simplified_lesk(word, sentence):
    stops = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    best = None
    best_sense_overlap = 0

    sent = sentence.lower()
    sentence_no_punc = sent.replace(".", "")
    tokenized_words = word_tokenize(sentence_no_punc)
    context = set(tokenized_words)
    context = {word for word in context if word not in stops}
    context = {lemmatizer.lemmatize(word) for word in context}
    #print(context)
    word_synsets = wn.synsets(word)

    for sense in word_synsets:
        signature = set(word_tokenize(sense.definition()))
        for example in sense.examples():
            signature.update(word_tokenize(example.lower()))

        signature = {word for word in signature if word not in stops}
        signature = {lemmatizer.lemmatize(word) for word in signature}
        #print(signature)
        current_overlap = compute_overlap(context, signature)
        #print(current_overlap)

        if current_overlap >= best_sense_overlap:
            best_sense_overlap = current_overlap
            best_sense = sense
            best_def = sense.definition()
    return best_def

def thesaurus(word):
    synonyms = []
    for i in wn.synsets(word):
        for j in i.lemmas():
            synonyms.append(j.name())

    return synonyms




#define("lexical")

