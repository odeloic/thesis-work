import pandas as pd
from summa.pagerank_weighted import pagerank_weighted_scipy as _pagerank
from summa.summarizer import _remove_unreachable_nodes
from summa.summarizer import _extract_most_important_sentences, _add_scores_to_sentences, _format_results
from summa.commons import build_graph
from summa.summarizer import _set_graph_edge_weights
from lib.clean_sentences import clean_sentences
from lib.stopwords import STOPWORDS
from rouge_score import rouge_scorer
df = pd.read_csv('Data/amakuru.csv')
test_article_content = str(df['Body'][300])
test_article_url = df['Url'][300]
test_article_golden_summary = """
Laura Musanase uzwi nka Nikuze muri film y’uruhererekane izwi nka City Maid, avuga ko yinjiye muri uyu mwuga atabishaka none ubu akaba amaze kwamamara kandi anabikunda.
"""

print(test_article_url)


def summarize_custom(text, ratio=0.2, split=False, scores=False, words=None, stopwords=None):
    cleaned_sentences = clean_sentences(text, stopwords=stopwords)
    graph = build_graph([sentence.token for sentence in cleaned_sentences])
    _set_graph_edge_weights(graph)
    _remove_unreachable_nodes(graph)
    pagerank_scores = _pagerank(graph)
    _add_scores_to_sentences(cleaned_sentences, pagerank_scores)
    extracted_sentences = _extract_most_important_sentences(
        cleaned_sentences, ratio, words)
    extracted_sentences.sort(key=lambda s: s.index)
    return _format_results(extracted_sentences, split, scores)


text_article_summary = summarize_custom(
    test_article_content, words=50, stopwords=STOPWORDS)
print(text_article_summary)


scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'])
scores = scorer.score(test_article_golden_summary, text_article_summary b/\
  )

print(scores)
