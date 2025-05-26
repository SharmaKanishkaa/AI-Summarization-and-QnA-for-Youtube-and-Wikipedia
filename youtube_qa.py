from fetch_transcript import fetch_transcript, preprocess_transcript
import re
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from typing import List, Optional
import logging

import toml


# Load API key from secrets.toml
secrets = toml.load("secrets.toml")
api_key = secrets["api"]["groq_api_key"]


def query_llama_model(api_key: str, prompt: str) -> Optional[str]:
    """
    Query the Groq API with the correct payload format.

    Args:
        api_key: Groq API key
        prompt: Input prompt

    Returns:
        Generated text response or None if failed
    """
    if not api_key:
        raise ValueError("API key is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",  # Updated to available model
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions about video content based on transcripts."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
        # Removed max_tokens as it's optional
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            logging.error(f"API Error: {response.status_code} - {response.text}")
            return None

        result = response.json()
        if not result.get("choices"):
            raise ValueError("No choices in response")

        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        return None
    except (KeyError, ValueError) as e:
        logging.error(f"Error parsing API response: {str(e)}")
        return None

def youtube_qa_system(video_url: str, question: str, api_key: str) -> str:
    """
    Main QA system with improved error handling and response formatting.

    Args:
        video_url: YouTube video URL
        question: User question
        api_key: Groq API key

    Returns:
        Answer string or error message
    """
    try:
        # Input validation
        if not video_url or not question or not api_key:
            raise ValueError("Missing required parameters")

        # Fetch transcript
        transcript = fetch_transcript(video_url)
        if not transcript:
            return "Could not extract transcript from video"

        # Process transcript
        chunks = preprocess_transcript(transcript)
        if not chunks:
            return "Failed to process transcript"

        # Prepare prompt with better formatting
        max_chunks=10
        context = " ".join(chunks[:max_chunks])
        prompt = (
            f"Based on the following video transcript, please answer the question.\n\n"
            f"Transcript: {context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )

        # Get model response
        answer = query_llama_model(api_key, prompt)
        if not answer:
            return "Failed to generate answer"

        return answer

    except Exception as e:
        logging.error(f"Error in QA system: {str(e)}")
        return f"An error occurred: {str(e)}"
    
# # Example usage
# if __name__ == "__main__":
#     video_url = "https://youtu.be/tbnzAVRZ9Xc?feature=shared"
#     question = "what conclusion came out from this video"
#     groq_api_key = "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"  # Replace with actual API key

#     logging.basicConfig(level=logging.INFO)
#     answer = youtube_qa_system(video_url, question, groq_api_key)
#     print("Answer:", answer)

# from fetch_transcript import fetch_transcript, preprocess_transcript
# import requests

# def query_llama_model(api_key, prompt):
#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
#     payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "Assistant."}, {"role": "user", "content": prompt}]}
#     response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
#     return response.json()["choices"][0]["message"]["content"].strip()

# def youtube_qa_system(video_url, question, api_key):
#     transcript = fetch_transcript(video_url)
#     chunks = preprocess_transcript(transcript)
#     context = " ".join(chunks)
#     prompt = f"Transcript: {context}\n\nQuestion: {question}\n\nAnswer:"
#     return query_llama_model(api_key, prompt)
