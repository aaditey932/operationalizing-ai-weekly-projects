"""RAG chain implementation using LangChain."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import config


class RAGChain:
    """RAG (Retrieval-Augmented Generation) chain implementation."""
    
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE
        )
        self.prompt = self._create_prompt()
        self.chain = self._build_chain()
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the prompt template for RAG."""
        return PromptTemplate(
            template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is insufficient, just say you don't know.

            {context}
            Question: {question}
            """,
            input_variables=['context', 'question']
        )
    
    def _format_docs(self, retrieved_docs):
        """Format retrieved documents into context string."""
        return "\n\n".join(doc.page_content for doc in retrieved_docs)
    
    def _build_chain(self):
        """Build the complete RAG chain."""
        parallel_chain = RunnableParallel({
            'context': self.retriever | RunnableLambda(self._format_docs),
            'question': RunnablePassthrough()
        })
        
        parser = StrOutputParser()
        
        return parallel_chain | self.prompt | self.llm | parser
    
    def query(self, question: str) -> str:
        """
        Query the RAG system with a question.
        
        Args:
            question: Question to ask about the document
            
        Returns:
            Generated answer based on retrieved context
        """
        return self.chain.invoke(question)
    
    def get_context(self, question: str) -> str:
        """
        Get the retrieved context for a question (for debugging).
        
        Args:
            question: Question to retrieve context for
            
        Returns:
            Retrieved context as formatted string
        """
        retrieved_docs = self.retriever.invoke(question)
        return self._format_docs(retrieved_docs)