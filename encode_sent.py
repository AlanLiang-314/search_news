from bidict import bidict
from sentence_transformers import SentenceTransformer, util
import os
from fetch_news import fetch
import pickle
import numpy as np

embedding_path = "embeddings/data.pkl"

bi_encoder = SentenceTransformer("models/shibing624_text2vec-base-chinese",device='cuda')


passages, text_id = fetch("https://www.twreporter.org/a/opinion-lower-voting-age-to-18-japan-expenrience")


corpus_embeddings = bi_encoder.encode(
            passages, show_progress_bar=True, device='cuda')


text_ids = [text_id]*len(passages)
if not os.path.exists(embedding_path):
    with open(embedding_path, 'wb') as fIn:
        pickle.dump({'sents':passages, 'embeddings':corpus_embeddings, 'uuid':text_ids},fIn)
else:
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