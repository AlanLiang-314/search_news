from sentence_transformers import SentenceTransformer
from fetch_news import fetch
import torch
from const import EMBEDDING_PATH
import emb


embedder = emb.embedder(EMBEDDING_PATH)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bi_encoder = SentenceTransformer(
    "models/shibing624_text2vec-base-chinese", device=device)


def encode(url: str):

    passages, text_id = fetch(url)

    corpus_embeddings = bi_encoder.encode(
        passages, show_progress_bar=True, device='cuda')

    # save to data.pkl
    text_ids = [text_id]*len(passages)

    if len(passages):
        embedder.write(passages, corpus_embeddings, text_ids)
        embedder.save()


encode("https://www.twreporter.org/a/sars-cov-2-variants")
