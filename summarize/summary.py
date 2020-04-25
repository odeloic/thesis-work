from summarize.utils import getTFIDF, score_sentence, get_sorted_sentences, score_document, get_top_sentences, build_summary, getWordsFreq
from nltk.tokenize import sent_tokenize
from heapq import nlargest
from summa.pagerank_weighted import pagerank_weighted_scipy as _pagerank
from summa.summarizer import _remove_unreachable_nodes
from summa.summarizer import _extract_most_important_sentences, _add_scores_to_sentences, _format_results
from lib.clean_sentences import clean_sentences
from summa.summarizer import _set_graph_edge_weights
from summa.commons import build_graph


def build_summary_using_tfidf(text, stopwords, nsentences):
    # calculate tfidf score
    sentences = sent_tokenize(text)
    # remove duplicate sentences
    sentences = list(dict.fromkeys(sentences))
    tfidf_dict = getTFIDF(text, stopwords)
    print(nlargest(10, tfidf_dict))
    sentence_scores = score_document(text, tfidf_dict, stopwords)
    for score in sentence_scores:
        print(f'score: {sentence_scores[score]}')
    sorted_sentences = get_sorted_sentences(sentence_scores)
    top_sentences = sorted(get_top_sentences(sorted_sentences, nsentences))
    print(f'Chosen sentences: {top_sentences}')
    build_summary(sentences, sorted(top_sentences))


def build_summary_using_wordsFreq(text, stopwords, nsentences):
    # get words frequency
    sentences = sent_tokenize(text)
    wordsFreq = getWordsFreq(text, stopwords)
    sentence_scores = score_document(text, wordsFreq, stopwords)
    sorted_sentences = get_sorted_sentences(sentence_scores)
    top_sentences = get_top_sentences(sorted_sentences, nsentences)
    print(f'Chosen sentences: {top_sentences}')
    build_summary(sentences, top_sentences)


def build_summary_using_txtrank(text, ratio=0.2, split=False, scores=False, words=None, stopwords=None):
    cleaned_sentences = clean_sentences(text, stopwords=stopwords)
    graph = build_graph([sentence.token for sentence in cleaned_sentences])
    _set_graph_edge_weights(graph)
    _remove_unreachable_nodes(graph)
    pagerank_scores = _pagerank(graph)
    _add_scores_to_sentences(cleaned_sentences, pagerank_scores)
    extracted_sentences = _extract_most_important_sentences(
        cleaned_sentences, ratio, words)
    extracted_sentences.sort(key=lambda s: s.index)
    return _format_results(extracted_sentences, split, scores), graph
