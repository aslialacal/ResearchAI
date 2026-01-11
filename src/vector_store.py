

# Setup ChromaDB vector database (downloaded in terminal as always)

import chromadb
from chromadb.config import Settings
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory= str(Path(__file__).parent.parent / "data" / "chroma_db")
        ))
        self.collection =self.client.get_or_create_collection("research_papers")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def add_papers(self, papers):
     """Adding papers too vector database with embeddings"""
     for paper in papers:
         text = f"{paper['title']} {paper['summary']}"
         embedding = self.model.encode(text).tolist()
         
         self.collection.add( embeddings=[embedding], documents=[paper['summary']], 
                            metadatas = [{"title": paper['title'], "authors": ",".join(paper['authors'])}],
                            ids= [paper['arxiv_id']]
                            )
        
         
    def search_similar (self, query, n_results=5):    #remember : use 5 only if no value is passed in my main pipeline
        """search for similar papers using semantic similarity"""
        query_embedding = self.model.encode (query).tolist()
        results= self.collection.query( query_embeddings=[query_embedding], n_results= n_results)
        return results