from sentence_transformers import SentenceTransformer
import os
from fetch_news import fetch
import pickle
import numpy as np

embedding_path = "embeddings/data.pkl"

bi_encoder = SentenceTransformer("models/shibing624_text2vec-base-chinese",device='cuda')


def encode(url: str):

    passages, text_id = fetch(url)


    corpus_embeddings = bi_encoder.encode(
                passages, show_progress_bar=True, device='cuda')


    # save to data.pkl
    text_ids = [text_id]*len(passages)
    if not os.path.exists(embedding_path):
        with open(embedding_path, 'wb') as fIn:
            pickle.dump({'sents':passages, 'embeddings':corpus_embeddings, 'uuid':text_ids},fIn)
    else:
        # check if the passages is empty
        if len(passages):
            with open(embedding_path, 'rb') as fOut:
                data = pickle.load(fOut)
                sent_emb = data['embeddings']
                sents = data['sents']
                ids = data['uuid']
            
            sents.extend(passages)
            sent_emb = np.concatenate([sent_emb, corpus_embeddings])
            ids.extend(text_ids)
            
            with open(embedding_path, 'wb') as fIn:
                pickle.dump({'sents':sents, 'embeddings':sent_emb, 'uuid':ids},fIn)



encode("https://www.twreporter.org/a/opinion-covid-19-global-health-governance-challenge")