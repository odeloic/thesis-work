import pickle
import nltk
import os
import re
import math
from math import floor
import operator
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from lib.kinya_norm import normalize_text
Stopwords = set(stopwords.words('english'))
wordlemmatizer = WordNetLemmatizer()


def remove_special_characters(text):
    regex = r'[^a-zA-Z0-9\s]'
    text = re.sub(regex, '', text)
    return text


def freq(words):
    words = [word.lower() for word in words]
    dict_freq = {}
    words_unique = []
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        dict_freq[word] = words.count(word)
    return dict_freq


def tf_score(word, sentence):
    word_frequency_in_sentence = 0
    len_sentence = len(sentence)
    for word_in_sentence in sentence.split():
        if word == word_in_sentence:
            word_frequency_in_sentence = word_frequency_in_sentence + 1
    tf = word_frequency_in_sentence / len_sentence
    return tf


def idf_score(no_of_sentences, word, sentences, Stopwords):
    no_of_sentence_containing_word = 0
    for sentence in sentences:
        sentence = remove_special_characters(str(sentence))
        sentence = re.sub(r'\d+', '', sentence)
        sentence = sentence.split()
        sentence = [word for word in sentence if word.lower()
                    not in Stopwords and len(word) > 1]
        sentence = [word.lower() for word in sentence]
        if word in sentence:
            no_of_sentence_containing_word = no_of_sentence_containing_word + 1
    idf = math.log10(no_of_sentences/no_of_sentence_containing_word)
    return idf


def tf_idf_score(tf, idf):
    return tf*idf


def word_tfidf(dict_freq, word, sentences, sentence, Stopwords):
    tf = tf_score(word, sentence)
    idf = idf_score(len(sentences), word, sentences, Stopwords)
    tf_idf = tf_idf_score(tf, idf)
    return tf_idf


def sentence_importance(title='', sentence='', position=None, dict_freq={}, sentences=[], Stopwords=None, score_title=False, score_position=False, minPos=None):
    sentence_score = 0
    sentence = remove_special_characters(str(sentence))
    sentence = re.sub(r'\d+', '', sentence)
    words_in_title = [word for word in word_tokenize(
        normalize_text(title, remove_digits=False, stopwords_removal=True, stopwords=Stopwords))]
    for word in word_tokenize(sentence):
        if word.lower() not in Stopwords and word not in Stopwords and len(word) > 1:
            word = word.lower()
            sentence_score = sentence_score + \
                word_tfidf(dict_freq, word, sentences, sentence, Stopwords)
        if score_title and title and word.lower() in words_in_title:
            sentence_score += len(words_in_title)
    if score_position and position and position < minPos:
        sentence_score += len(sentences)

    return sentence_score


def summariza_tfidf(title='', text='', ratio=0.3, Stopwords=None, score_title=False, score_position=False):
    tokenized_sentence = sent_tokenize(text)
    # remove duplicates
    tokenized_sentence = list(dict.fromkeys(tokenized_sentence))
    no_sentences = floor(len(tokenized_sentence)*ratio)
    text = remove_special_characters(str(text))
    text = re.sub(r'\d+', '', text)
    tokenized_words_with_stopwords = word_tokenize(text)
    tokenized_words = [
        word for word in tokenized_words_with_stopwords if word not in Stopwords]
    tokenized_words = [word for word in tokenized_words if len(word) > 1]
    tokenized_words = [word.lower() for word in tokenized_words]
    word_freq = freq(tokenized_words)
    c = 1
    sentence_with_importance = {}
    n_sentences = floor(len(tokenized_sentence)*ratio)
    for i, sent in enumerate(tokenized_sentence):
        sentenceimp = sentence_importance(
            title, sent, i, word_freq, tokenized_sentence, Stopwords, score_title, score_position, minPos=n_sentences)
        sentence_with_importance[c] = sentenceimp
        c = c+1
    sentence_with_importance = sorted(
        sentence_with_importance.items(), key=operator.itemgetter(1), reverse=True)
    cnt = 0
    summary = []
    sentence_no = []
    for word_prob in sentence_with_importance:
        if cnt < no_sentences:
            sentence_no.append(word_prob[0])
            cnt = cnt+1
        else:
            break
    sentence_no.sort()
    cnt = 1
    indices = []
    for i, sentence in enumerate(tokenized_sentence):
        if cnt in sentence_no:
            summary.append(sentence)
            indices.append(i)
        cnt = cnt+1
    summary = " ".join(summary)
    print(f"selected sentences: {indices}")
    return summary


=
