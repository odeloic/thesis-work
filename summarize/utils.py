from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import os
import sys
import pickle
import pandas as pd
from lib.kinya_norm import normalize_text
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


def getTFIDF(text, stopwords):
    # preprocess document
    doc = normalize_text(text, stopwords_removal=True, stopwords=stopwords)
    # get clean sentences tokens
    clean_sentences_tokens = sent_tokenize(doc)
    cv = CountVectorizer(tokenizer=word_tokenize)
    # create word counts for the words in document
    word_count_vector = cv.fit_transform(clean_sentences_tokens)
    tfidf_transformer_vector = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer_vector.fit(word_count_vector)

    # calculate tfidf
    count_vector = cv.transform(clean_sentences_tokens)
    tf_idf_vector = tfidf_transformer_vector.transform(count_vector)
    feature_names = cv.get_feature_names()
    df = pd.DataFrame(tf_idf_vector.todense().tolist(), columns=feature_names)
    return df.T.to_dict('dict')[0]


def score_sentence(sentence, cdict, stopwords):
    sentence_score = 0
    clean_sentences = normalize_text(
        sentence, stopwords_removal=True, stopwords=stopwords)
    for word in word_tokenize(clean_sentences):
        if word.lower() not in stopwords and word not in stopwords and len(word) > 1:
            sentence_score += cdict[word.lower()]
    return sentence_score


def get_sorted_sentences(sentence_scores):
    return sorted(sentence_scores.items(), key=lambda x: x[1])


def score_document(document, cdict, stopwords):
    sentences = sent_tokenize(document)
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_scores[i] = score_sentence(sentence, cdict, stopwords)
    return sentence_scores


def get_top_sentences(sentences, nsentences):
    top_sentences = []
    for n in range(0, nsentences):
        top_sentences.append(sentences[n][0])
    return top_sentences


def build_summary(original_sentences, top_sentences):
    for i in top_sentences:
        print(original_sentences[i])


def getWordsFreq(text, stopwords):
    normalized_text = normalize_text(
        text, stopwords_removal=True, stopwords=stopwords)
    tokens = word_tokenize(normalized_text)
    wordsFreq = FreqDist(tokens)
    return wordsFreq
