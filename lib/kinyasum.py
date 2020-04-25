from nltk.tokenize import sent_tokenize, word_tokenize
from lib.helpers import getStopwordsFromFile
from lib.kinya_norm import remove_special_characters, normalize_text
from nltk.probability import FreqDist
import itertools
from math import floor


def summarize_text_(title='', text='', ratio=0.3, stopwords=[], score_title=True, score_position=True):
    '''
    This function summarizes a given text and return a small condensed content depending on the ratio provided
    return str
    '''
    # cleaned_text
    clean_text = normalize_text(
        text, stopwords_removal=True, stopwords=stopwords)
    # get words in title
    words_in_title = [word for word in word_tokenize(
        normalize_text(title, stopwords_removal=True, stopwords=stopwords))]
    # get sentece tokens
    original_sentences = sent_tokenize(text)
    # remove duplicates
    original_sentences = list(dict.fromkeys(original_sentences))
    n_sentences = floor(len(original_sentences)*ratio)
    # get words frequency distribution
    wordsFreq = FreqDist(word_tokenize(clean_text))
    scoreDict = {}
    for i, sent in enumerate(original_sentences):
        score_sentence = 0
        for word in word_tokenize(normalize_text(sent, stopwords_removal=True, stopwords=stopwords)):
            score_sentence += wordsFreq[word]
            if score_title and word.lower() in words_in_title:
                score_sentence += len(words_in_title)
        if score_position and i < n_sentences:
            score_sentence += len(original_sentences)
        score_sentence = score_sentence / len(sent)
        scoreDict[i] = score_sentence
    sortedSentences = {k: v for k, v in sorted(
        scoreDict.items(), key=lambda item: item[1], reverse=True)}
    topSentences = list(
        dict(itertools.islice(sortedSentences.items(), n_sentences)).keys())
    summary = ''
    print(f'selected sentences: {topSentences}')
    for i in topSentences:
        summary += ' ' + original_sentences[i]
    return summary
