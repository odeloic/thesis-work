from nltk.tokenize import sent_tokenize
from .kinya_norm import normalize_text
from summa.preprocessing.textcleaner import merge_syntactic_units
from summa.summarizer import _remove_unreachable_nodes
from summa.summarizer import _extract_most_important_sentences, _add_scores_to_sentences
from summa.pagerank_weighted import pagerank_weighted_scipy as _pagerank
from summa.summarizer import _set_graph_edge_weights
from summa.commons import build_graph


def clean_sentences(text, stopwords=None):
    """
    Tokenize a given text into sentences, and removing stopwords
    """
    text = text.replace('\n', '')
    original_sentences = text.split('.')
    original_sentences = list(dict.fromkeys(original_sentences))
    cleaned_sentences = [normalize_text(
        stopwords_removal=True, stopwords=stopwords, doc=s) for s in original_sentences]
    return merge_syntactic_units(original_sentences, cleaned_sentences)


def _format_results(extracted_sentences, split, score):
    selected_sentneces = [sentence.index for sentence in extracted_sentences]
    print(f'selected sentences: {sorted(selected_sentneces)}')
    if score:
        return [(sentence.text, sentence.score) for sentence in extracted_sentences]
    if split:
        return [sentence.text for sentence in extracted_sentences]
    return ". ".join([sentence.text for sentence in extracted_sentences])


def summariza_textrank(text, ratio=0.3, split=False, scores=False, words=None, stopwords=None):
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


# a_body = '''
# Banki y’Ubucuruzi ya Cogebanque yashyikirije MTN Rwanda telefone zigezweho 1000 zizahabwa Abanyarwanda batishoboye muri gahunda ya Connect Rwanda, igamije kugeza smartphones ku badafite ubushobozi bwo kuzigurira.\nBanki y’Ubucuruzi ya Cogebanque yashyikirije MTN Rwanda telefone zigezweho 1000 zizahabwa Abanyarwanda batishoboye muri gahunda ya Connect Rwanda, igamije kugeza smartphones ku badafite ubushobozi bwo kuzigurira.\nKu mugoroba wo kuri uyu wa Kane tariki 12 Werurwe, nibwo abayobozi ba Cogebanque bashyikirije MTN Rwanda telefone 1000 mu rwego rwo gutanga umusanzu wayo mu kwihutisha ikoranabuhanga mu banyarwanda.\nKu wa 20 Ukuboza 2019 nibwo MTN Rwanda yatangije ubukangurambaga bwa Connect Rwanda, ibigo n’abantu ku giti cyabo batangira kwiyemeza umubare wa telefoni zigezweho bazatanga zigahabwa abaturage badafite ubushobozi bwo kuzigura mu turere dutandukanye, nibura imwe muri buri rugo.\nKuva icyo gihe ibigo bitandukanye n’abantu ku giti cyabo bahise batangira kwiyemeza izo bazatanga, abandi bakazitanga cyangwa bagatanga amafaranga yo kuzigura.\nUretse gushyigikira iyi gahunda ya Connect Rwanda, Cogebanque ikomeje gahunda zitadukanye zigamike guteza imbere ikoranabuhanga.\nYagabye amashami 28, ifite aba-agents barenga 600, ikaba ifite serivisi zitandukanye zitangwa hifashishijwe ikoranabuhanga ririmo amakarita, internet banking ndetse na telefone (Mobile banking, Mobile App na push & pull).\nNi serivisi yifashishwa n’abakiliya b’iyi banki mu kuba babona uko konti zabo zihagaze mu gihe havuyeho amafaranga cyangwa yongewe kuri konti, ishobora kandi kwifashihwa mu kwishyura fagitire z’amazi n’umuriro ndetse uyikoresha ashobora no kwiyoherereza amafaranga yo guhamagaza kuri telefone.\nCogebanque itanga Serivisi Mpuzamahanga binyuze mu ikoranabuhanga mu korohereza abanyarwanda kwizigamira nkuko biri muri gahunda za leta.\n
# '''
# ss = summariza_textrank(a_body, ratio=0.3)
# print(ss)
