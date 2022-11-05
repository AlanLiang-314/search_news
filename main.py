from sentence_transformers import SentenceTransformer, util
from fetch_news import fetch
from const import EMBEDDING_PATH, URL_PATH
from pprint import pprint
import save
import emb


pickler = save.pickler(URL_PATH)
embedder = emb.embedder(EMBEDDING_PATH)
bi_encoder = SentenceTransformer(
    "models/shibing624_text2vec-base-chinese", device='cuda')


def reload_embeddings():
    global sent_emb, sents, ids
    sent_emb, sents, ids = embedder.read()


def encode(url: str):

    passages, text_id = fetch(url)

    corpus_embeddings = bi_encoder.encode(
        passages, show_progress_bar=True, device='cuda')

    # save to data.pkl
    text_ids = [text_id]*len(passages)

    if len(passages):
        embedder.write(passages, corpus_embeddings, text_ids)
        embedder.save()


def search(query: str):
    query = query.split("|")
    # Encode text descriptions
    query_emb = bi_encoder.encode(query)

    if len(query_emb) > 1:
        query_emb = query_emb[0]-query_emb[1]
    else:
        query_emb = query_emb[0]

    # Compute cosine similarities
    hits = util.semantic_search(
        query_emb, sent_emb, top_k=5, score_function=util.cos_sim)[0]

    for hit in hits:
        pprint(sents[hit['corpus_id']])
        pprint(pickler.find_by_id(ids[hit['corpus_id']]))
