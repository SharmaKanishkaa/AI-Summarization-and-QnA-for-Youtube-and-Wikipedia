from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import re
from typing import List

class TranscriptError(Exception):
    """Custom exception for transcript-related errors."""
    pass

def fetch_transcript(video_url: str, preferred_languages: List[str] = ['en'], target_language: str = 'en') -> str:
    """
    Fetch transcript from YouTube video URL with better error handling and validation.
    Translates the transcript to the target language if it is not in the preferred languages.

    Args:
        video_url: YouTube video URL.
        preferred_languages: List of preferred language codes (default is ['en']).
        target_language: The language code to translate the transcript to if not in preferred languages.

    Returns:
        str: Combined transcript text, translated to the target language if needed.

    Raises:
        TranscriptError: If transcript cannot be fetched or processed.
    """
    try:
        # Improved regex pattern to handle more YouTube URL formats
        video_id_match = re.search(
            r"(?:v=|\/|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})",
            video_url
        )
        if not video_id_match:
            raise TranscriptError("Invalid YouTube URL format")

        video_id = video_id_match.group(1)

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Try to get transcript in preferred languages
            transcript = None
            for lang in preferred_languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    break
                except Exception:
                    continue

            # If no manual transcript, try auto-generated transcripts
            if not transcript:
                for lang in preferred_languages:
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        break
                    except Exception:
                        continue

            if not transcript:
                raise TranscriptError("No transcripts found in the preferred languages")

            transcript_data = transcript.fetch()
            combined_transcript = " ".join(item['text'] for item in transcript_data)

            # Translate if the transcript language is not the target language
            if transcript.language_code != target_language:
                print(f"Translating transcript from {transcript.language_code} to {target_language}...")
                translator = Translator()
                combined_transcript = translator.translate(combined_transcript, dest=target_language).text

            return combined_transcript

        except Exception as e:
            available_transcripts = []
            try:
                available_transcripts = [
                    t.language_code for t in transcript_list.manual_transcripts
                ]
            except:
                pass

            raise TranscriptError(
                f"Failed to fetch transcript. Available languages: {available_transcripts}. Error: {str(e)}"
            )

    except Exception as e:
        raise TranscriptError(f"Error processing video: {str(e)}")

def preprocess_transcript(transcript: str, chunk_size: int = 200) -> List[str]:
    """
    Preprocess transcript into chunks with improved text splitting.

    Args:
        transcript: Input transcript text.
        chunk_size: Maximum size of each chunk.

    Returns:
        List of text chunks.
    """
    # Split on sentence boundaries instead of just spaces
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', transcript) if s.strip()]
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Example usage
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=mOMeCmCdj7I"  # Replace with your video URL
    try:
        transcript = fetch_transcript(video_url, preferred_languages=['en', 'hi'], target_language='en')
        print("Transcript fetched successfully!")
        print(transcript)

        # Preprocess the transcript
        chunks = preprocess_transcript(transcript)
        print("\nProcessed Transcript Chunks:")
        for i, chunk in enumerate(chunks, 1):
            print(f"Chunk {i}: {chunk}")

    except TranscriptError as te:
        print(f"Transcript error: {str(te)}")

