#%%
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
# model = SentenceTransformer("quora-distilbert-base")
print("libraries imported")
#%%

class QuestionAnswering:

    def __init__(self, lang):
        self.lang = lang
        print("QuestionAnswering class initialized ..... ", lang)
    
    def load_model_func(self):
        if self.lang=="tr":
            model_path = "models/savasy_bert-base-turkish-sentiment-cased"
            df_path = "data/tr/df_faq_with_embeddings.csv"
        elif self.lang=="en":
            # model_path = "models/sentence-transformers_quora-distilbert-base"
            model_path = "models/flax-sentence-embeddings_all_datasets_v3_mpnet-base"
            df_path = "data/en/df_faq_with_embeddings.csv"        
        model = SentenceTransformer(model_path)
        df = pd.read_csv(df_path)
        return model, df
    
    def load_model(self):
        self.model, self.df = self.load_model_func()
        print("model loaded ..... ", self.lang)

    def get_best(self, query):
        # self.model, self.df = self.load_model_func()
        faq_embeddings = self.df.iloc[:,2:]
        faq = self.df.Question
        faq_answers = self.df.Answer
        query_embedding = self.model.encode([query])
        distances = cdist(query_embedding, faq_embeddings, "cosine")[0]
        ind = np.argsort(distances, axis=0)
        return distances, ind, faq, faq_answers
    
