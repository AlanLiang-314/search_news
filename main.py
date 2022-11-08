from sentence_transformers import SentenceTransformer, util
from fastapi import FastAPI
from fetch_news import fetch
from const import EMBEDDING_PATH, URL_PATH
import save
import emb


pickler = save.pickler(URL_PATH)
embedder = emb.embedder(EMBEDDING_PATH)
bi_encoder = SentenceTransformer(
    "models/shibing624_text2vec-base-chinese", device='cuda')


# ===== FastAPI =====

app = FastAPI()


@app.get("/reload")
async def reload_embeddings():
    # discarded
    global sent_emb, sents, ids
    sent_emb, sents, ids = embedder.read()


@app.get("/encode")
async def encode(url: str):

    passages, text_id = fetch(url)

    corpus_embeddings = bi_encoder.encode(
        passages, show_progress_bar=True, device='cuda')

    # save to data.pkl
    text_ids = [text_id]*len(passages)

    if len(passages):
        embedder.write(passages, corpus_embeddings, text_ids)
        embedder.save()

    return True


@app.get("/search")
def search(query: str):
    query = query.split("|")
    # Encode text descriptions
    query_emb = bi_encoder.encode(query)

    if len(query_emb) > 1:
        query_emb = query_emb[0]-query_emb[1]
    else:
        query_emb = query_emb[0]

    sent_emb, sents, ids = embedder.read()
    # Compute cosine similarities
    hits = util.semantic_search(
        query_emb, sent_emb, top_k=5, score_function=util.cos_sim)[0]

    result = {}
    i = 1
    for hit in hits:
        sent = sents[hit['corpus_id']]
        id = pickler.find_by_id(ids[hit['corpus_id']])
        # pprint(sents[hit['corpus_id']])
        # pprint(pickler.find_by_id(ids[hit['corpus_id']]))
        result[i] = {"sentence": sent, "id": id}
        i += 1

    return result
