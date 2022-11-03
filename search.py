from sentence_transformers import SentenceTransformer, util
import pickle
import save
from pprint import pprint

embedding_path = "embeddings/data.pkl"

pickler = save.pickler("urls/urls.pkl")

bi_encoder = SentenceTransformer("models/shibing624_text2vec-base-chinese", device='cpu')

def load_embeddings():
    global sent_emb, sents, ids
    with open(embedding_path, 'rb') as fIn:
            data = pickle.load(fIn)
            sent_emb = data['embeddings']
            sents = data['sents']
            ids = data['uuid']

load_embeddings()

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
            query_emb, sent_emb, top_k=4, score_function=util.cos_sim)[0]
    
    for hit in hits:
        #pprint("{} , cos_sim: {:.2f}".format(sents[hit['corpus_id']], hit['score']))
        #pprint("{} , uuid: {}".format(sents[hit['corpus_id']], ids[hit['corpus_id']]))
        pprint(sents[hit['corpus_id']])
        pprint(pickler.find_by_id(ids[hit['corpus_id']]))