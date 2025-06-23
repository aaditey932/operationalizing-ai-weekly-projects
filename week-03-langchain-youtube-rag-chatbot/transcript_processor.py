"""YouTube transcript processing utilities."""

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional
import config


class TranscriptProcessor:
    """Handles YouTube transcript extraction and processing."""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
    
    def extract_transcript(self, video_id: str, languages: List[str] = None) -> Optional[str]:
        """
        Extract transcript from YouTube video.
        
        Args:
            video_id: YouTube video ID (not full URL)
            languages: List of preferred languages (default: ["en"])
            
        Returns:
            Transcript text as string, or None if not available
        """
        if languages is None:
            languages = ["en"]
            
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            return transcript
        except TranscriptsDisabled:
            print(f"No captions available for video: {video_id}")
            return None
        except Exception as e:
            print(f"Error extracting transcript: {e}")
            return None
    
    def split_text(self, text: str):
        """
        Split text into chunks for processing.
        
        Args:
            text: Input text to split
            
        Returns:
            List of document chunks
        """
        return self.text_splitter.create_documents([text])