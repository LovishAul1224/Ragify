from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL

class EmbeddingModel:
     """Creates embeddings for documents."""
     def __init__(self):
          self.embeddings = HuggingFaceEmbeddings(
               model_name = EMBEDDING_MODEL
        )
     
     def get_embeddings(self):
          return self.embeddings
    

## Here the model we are using is sentence-transformers/all-MiniLM-L6-v2
##   it's a free model, Runs locally and it is fast.
##   it  Produces 384-dimensional vectors
