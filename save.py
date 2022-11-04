from secrets import token_urlsafe
from bidict import bidict
import pickle
import os


class pickler:

    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'wb') as fOut:
                pickle.dump(bidict({}),fOut)
        
        with open(self.path, 'rb') as fIn:
            self.data = pickle.load(fIn)
   

    def add(self, text: str):
        #values = self.data.values()
        id = token_urlsafe(16)

        if not text in self.data.inverse:
            self.data[id] = text
            return id
        else:
            #print("the file already exists")
            return None

    def update(self):
        pass

    def delete_by_id(self, id):
        del self.data[id]

    def delete_by_text(self, text):
        del self.data.inverse[text]

    def save(self):
        with open(self.path, 'wb') as fOut:
            pickle.dump(self.data,fOut)

    def show(self):
        print(self.data)
        return self.data

    def find_by_id(self, id: str):
        return self.data.get(id)

    def find_by_text(self, text):
        return self.data.inverse.get(text)
    

