"""Vector store management for RAG system."""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
import config


class VectorStoreManager:
    """Manages vector store operations for document embeddings."""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.vector_store = None
    
    def create_vector_store(self, documents: List):
        """
        Create vector store from documents.
        
        Args:
            documents: List of document chunks to embed
            
        Returns:
            FAISS vector store
        """
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def get_retriever(self):
        """
        Get retriever from vector store.
        
        Returns:
            Document retriever configured for similarity search
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        return self.vector_store.as_retriever(
            search_type=config.SEARCH_TYPE,
            search_kwargs={"k": config.RETRIEVAL_K}
        )
    
    def save_vector_store(self, path: str):
        """Save vector store to disk."""
        if self.vector_store:
            self.vector_store.save_local(path)
    
    def load_vector_store(self, path: str):
        """Load vector store from disk."""
        self.vector_store = FAISS.load_local(path, self.embeddings)
        return self.vector_store