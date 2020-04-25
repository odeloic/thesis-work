from nltk.tokenize import sent_tokenize
from .kinya_norm import normalize_text
from summa.preprocessing.textcleaner import merge_syntactic_units


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


a_body = '''
Banki y’Ubucuruzi ya Cogebanque yashyikirije MTN Rwanda telefone zigezweho 1000 zizahabwa Abanyarwanda batishoboye muri gahunda ya Connect Rwanda, igamije kugeza smartphones ku badafite ubushobozi bwo kuzigurira.\nBanki y’Ubucuruzi ya Cogebanque yashyikirije MTN Rwanda telefone zigezweho 1000 zizahabwa Abanyarwanda batishoboye muri gahunda ya Connect Rwanda, igamije kugeza smartphones ku badafite ubushobozi bwo kuzigurira.\nKu mugoroba wo kuri uyu wa Kane tariki 12 Werurwe, nibwo abayobozi ba Cogebanque bashyikirije MTN Rwanda telefone 1000 mu rwego rwo gutanga umusanzu wayo mu kwihutisha ikoranabuhanga mu banyarwanda.\nKu wa 20 Ukuboza 2019 nibwo MTN Rwanda yatangije ubukangurambaga bwa Connect Rwanda, ibigo n’abantu ku giti cyabo batangira kwiyemeza umubare wa telefoni zigezweho bazatanga zigahabwa abaturage badafite ubushobozi bwo kuzigura mu turere dutandukanye, nibura imwe muri buri rugo.\nKuva icyo gihe ibigo bitandukanye n’abantu ku giti cyabo bahise batangira kwiyemeza izo bazatanga, abandi bakazitanga cyangwa bagatanga amafaranga yo kuzigura.\nUretse gushyigikira iyi gahunda ya Connect Rwanda, Cogebanque ikomeje gahunda zitadukanye zigamike guteza imbere ikoranabuhanga.\nYagabye amashami 28, ifite aba-agents barenga 600, ikaba ifite serivisi zitandukanye zitangwa hifashishijwe ikoranabuhanga ririmo amakarita, internet banking ndetse na telefone (Mobile banking, Mobile App na push & pull).\nNi serivisi yifashishwa n’abakiliya b’iyi banki mu kuba babona uko konti zabo zihagaze mu gihe havuyeho amafaranga cyangwa yongewe kuri konti, ishobora kandi kwifashihwa mu kwishyura fagitire z’amazi n’umuriro ndetse uyikoresha ashobora no kwiyoherereza amafaranga yo guhamagaza kuri telefone.\nCogebanque itanga Serivisi Mpuzamahanga binyuze mu ikoranabuhanga mu korohereza abanyarwanda kwizigamira nkuko biri muri gahunda za leta.\n
'''
clean_sentences(a_body)
