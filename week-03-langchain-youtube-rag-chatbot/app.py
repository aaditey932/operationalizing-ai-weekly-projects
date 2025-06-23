"""Streamlit app for the RAG system."""

import streamlit as st
from transcript_processor import TranscriptProcessor
from vector_store_manager import VectorStoreManager
from rag_chain import RAGChain
import time


def initialize_session_state():
    """Initialize session state variables."""
    if 'rag_chain' not in st.session_state:
        st.session_state.rag_chain = None
    if 'video_processed' not in st.session_state:
        st.session_state.video_processed = False
    if 'current_video_id' not in st.session_state:
        st.session_state.current_video_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def extract_video_id(url_or_id):
    """Extract video ID from YouTube URL or return ID if already provided."""
    if 'youtube.com/watch?v=' in url_or_id:
        return url_or_id.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url_or_id:
        return url_or_id.split('youtu.be/')[1].split('?')[0]
    else:
        # Assume it's already a video ID
        return url_or_id


def process_video(video_input):
    """Process a YouTube video and create RAG chain."""
    video_id = extract_video_id(video_input)
    
    with st.spinner("Processing video..."):
        # Initialize components
        processor = TranscriptProcessor()
        vector_manager = VectorStoreManager()
        
        # Step 1: Extract transcript
        st.info("📥 Extracting transcript...")
        transcript = processor.extract_transcript(video_id)
        
        if not transcript:
            st.error("❌ Failed to extract transcript. Please check the video ID and ensure captions are available.")
            return False
        
        st.success(f"✅ Transcript extracted ({len(transcript)} characters)")
        
        # Step 2: Split text
        st.info("✂️ Splitting text into chunks...")
        chunks = processor.split_text(transcript)
        st.success(f"✅ Text split into {len(chunks)} chunks")
        
        # Step 3: Create vector store
        st.info("🔍 Creating vector embeddings...")
        vector_store = vector_manager.create_vector_store(chunks)
        st.success("✅ Vector store created")
        
        # Step 4: Initialize RAG chain
        st.info("🔗 Initializing RAG chain...")
        retriever = vector_manager.get_retriever()
        rag_chain = RAGChain(retriever)
        st.success("✅ RAG system ready!")
        
        # Store in session state
        st.session_state.rag_chain = rag_chain
        st.session_state.video_processed = True
        st.session_state.current_video_id = video_id
        st.session_state.chat_history = []
        
        return True


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="YouTube RAG Chat",
        page_icon="🎥",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🎥 YouTube RAG Chat System")
    st.markdown("Ask questions about any YouTube video using AI-powered retrieval!")
    
    # Sidebar for video input
    with st.sidebar:
        st.header("📺 Video Setup")
        
        video_input = st.text_input(
            "Enter YouTube URL or Video ID:",
            placeholder="https://youtube.com/watch?v=... or video_id",
            help="Paste a YouTube URL or just the video ID"
        )
        
        process_button = st.button("🚀 Process Video", type="primary")
        
        if process_button and video_input:
            if process_video(video_input):
                st.rerun()
        
        # Show current video status
        if st.session_state.video_processed:
            st.success(f"✅ Video processed: `{st.session_state.current_video_id}`")
            if st.button("🔄 Process New Video"):
                st.session_state.video_processed = False
                st.session_state.rag_chain = None
                st.session_state.current_video_id = None
                st.session_state.chat_history = []
                st.rerun()
        
        # Example questions
        if st.session_state.video_processed:
            st.header("💡 Example Questions")
            example_questions = [
                "Can you summarize the video?",
                "What are the main topics discussed?",
                "Who are the key people mentioned?",
                "What are the key takeaways?"
            ]
            
            for question in example_questions:
                if st.button(f"❓ {question}", key=f"example_{question}"):
                    st.session_state.current_question = question
    
    # Main content area
    if not st.session_state.video_processed:
        st.info("👈 Please enter a YouTube URL or video ID in the sidebar to get started!")
        
        # Show example
        st.markdown("### 🎯 How it works:")
        st.markdown("""
        1. **Enter a YouTube URL** in the sidebar
        2. **Click 'Process Video'** to extract and index the transcript
        3. **Ask questions** about the video content
        4. **Get AI-powered answers** based on the video transcript
        """)
        
        st.markdown("### 📝 Example:")
        st.code("https://youtube.com/watch?v=Gfr50f6ZBvo")
        
    else:
        # Chat interface
        st.header("💬 Chat with the Video")
        
        # Display chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
        
        # Question input
        question = st.chat_input("Ask a question about the video...")
        
        # Handle example question from sidebar
        if hasattr(st.session_state, 'current_question'):
            question = st.session_state.current_question
            delattr(st.session_state, 'current_question')
        
        if question:
            # Display user question
            with st.chat_message("user"):
                st.write(question)
            
            # Generate and display answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = st.session_state.rag_chain.query(question)
                st.write(answer)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer
            })
        
        # Show retrieved context (expandable)
        if st.session_state.chat_history:
            with st.expander("🔍 View Retrieved Context (Debug)"):
                last_question = st.session_state.chat_history[-1]["question"]
                context = st.session_state.rag_chain.get_context(last_question)
                st.text_area("Retrieved Context:", context, height=200)


if __name__ == "__main__":
    main()