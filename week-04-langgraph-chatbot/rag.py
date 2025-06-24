from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

sample_docs = [
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs. It extends LangChain with cyclic computation capabilities.",
        metadata={"source": "langgraph_docs"}
    ),
    Document(
        page_content="Python is a high-level programming language known for its simplicity and readability. It's widely used in AI and data science.",
        metadata={"source": "python_docs"}
    ),
    Document(
        page_content="Artificial Intelligence involves creating systems that can perform tasks that typically require human intelligence, such as learning and problem-solving.",
        metadata={"source": "ai_docs"}
    )
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(sample_docs)
vectorstore = FAISS.from_documents(chunks, embeddings)

def retrieve_docs(query: str, k: int = 2):
    """Retrieve relevant documents for a query."""
    return vectorstore.similarity_search(query, k=k)

def format_docs(docs):
    """Format documents for context."""
    return "\n\n".join([doc.page_content for doc in docs])