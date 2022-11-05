import pickle
import numpy as np
import os


class embedder:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'wb') as fOut:
                pickle.dump({}, fOut)

        with open(self.path, 'rb') as fIn:
            self.data = pickle.load(fIn)

    def read(self):
        sent_emb = self.data['embeddings']
        sents = self.data['sents']
        ids = self.data['uuid']
        return sent_emb, sents, ids

    def get(self):
        return self.data

    def write(self, sents: list, sents_emb: np.ndarray, ids: list):
        self.data['sents'].extend(sents)
        self.data['uuid'].extend(ids)
        self.data['embeddings'] = np.concatenate(
            [self.data['embeddings'], sents_emb])

    def save(self):
        with open(self.path, 'wb') as fIn:
            pickle.dump(self.data, fIn)
