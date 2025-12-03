from sentence_transformers import SentenceTransformer
import os
import numpy as np

class SemanticRetriever:
    def __init__(self, examples ,cache_path=None ,
                 local_emeding_model = None , local_device = "cpu" ):
        
        self.local_device = local_device
        self.local_emeding_model = local_emeding_model
        self.model = SentenceTransformer(self.local_emeding_model , 
                                         device= self.local_device)
        self.examples = examples
        
        if cache_path and os.path.exists(cache_path):
            self.embeddings = np.load(cache_path)
            print("Loaded embeddings from cache")
        else:
            questions = [ex.question for ex in self.examples]
            self.embeddings = self.model.encode(questions)
            if cache_path:
                np.save(cache_path, self.embeddings)
                print("Saved embeddings to cache")

    
    def get_similar(self, question, k=2):
        q_emb = self.model.encode([question])[0]
        scores = np.dot(self.embeddings, q_emb)
        indices = scores.argsort()[-k:][::-1]
        return [self.examples[i] for i in indices]