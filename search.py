from sentence_transformers import SentenceTransformer, util
from const import EMBEDDING_PATH, URL_PATH
import pickle
import emb
import save
from pprint import pprint


pickler = save.pickler(URL_PATH)

embedder = emb.embedder(EMBEDDING_PATH)

bi_encoder = SentenceTransformer("models/shibing624_text2vec-base-chinese", device='cpu')


sent_emb, sents, ids = embedder.read()

while True:
    query = input("please enter a prompt，| to split negative prompt: ")
    if query == '-1': break
    
    query = query.split("|")
    #Encode text descriptions
    query_emb = bi_encoder.encode(query)

    if len(query_emb)>1:
        query_emb = query_emb[0]-query_emb[1]
    else:
        query_emb = query_emb[0]

    #Compute cosine similarities 
    hits = util.semantic_search(
            query_emb, sent_emb, top_k=5, score_function=util.cos_sim)[0]
    
    for hit in hits:
        #pprint("{} , cos_sim: {:.2f}".format(sents[hit['corpus_id']], hit['score']))
        #pprint("{} , uuid: {}".format(sents[hit['corpus_id']], ids[hit['corpus_id']]))
        pprint(sents[hit['corpus_id']])
        pprint(pickler.find_by_id(ids[hit['corpus_id']]))