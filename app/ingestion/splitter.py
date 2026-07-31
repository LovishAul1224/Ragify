from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentSplitter:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

    def split_documents(
        self, 
        documents: list[Document])-> list[Document]:

        return self.splitter.split_documents(documents)
