import re
import logging
from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from scraper import scraper, preprocess_content


def query_llama_model(api_key: str, prompt: str) -> Optional[str]:
    """
    Queries the Groq API for a response based on the given prompt.

    Args:
        api_key: Groq API key.
        prompt: Input prompt for the model.

    Returns:
        The generated response from the model or None if there was an error.
    """
    if not api_key:
        raise ValueError("API key is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions about content based on provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            error_message = response.json().get("error", {}).get("message", "Unknown API error")
            logging.error(f"API Error: {response.status_code} - {error_message}")
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


def content_qa_system(url: str, question: str, api_key: str) -> str:
    """
    Handles content-based question answering for Wikipedia URLs.

    Args:
        url: Wikipedia URL.
        question: User's question.
        api_key: Groq API key.

    Returns:
        The answer to the user's question or an error message.
    """
    try:
        # Input validation
        if not url or not question or not api_key:
            raise ValueError("Missing required parameters")

        # Fetch content from the URL
        title, content = scraper(url)
        if not content:
            return "Could not extract content from the provided URL."

        # Process content into manageable chunks
        chunks = preprocess_content(content)
        if not chunks:
            return "Failed to process content into chunks."

        # Prepare the prompt for the model
        context = " ".join(chunks)[:6000]
        prompt = (
            f"Based on the following Wikipedia article, please answer the question.\n\n"
            f"Title: {title}\n\n"
            f"Content: {context}\n\n"
            f"Question: {question}\n\n"
            f"Answer:"
        )

        # Query the model for an answer
        answer = query_llama_model(api_key, prompt)
        if not answer:
            return "Failed to generate an answer."

        return f"{answer}"

    except Exception as e:
        logging.error(f"Error in content QA system: {str(e)}")
        return f"An error occurred: {str(e)}"


# # Example usage
# if __name__ == "__main__":
#     example_url = "https://en.wikipedia.org/wiki/Natural_language_processing"
#     example_question = "What is natural language processing used for?"
#     groq_api_key = "your_api_key_here"  # Replace with your actual API key

#     answer = content_qa_system(example_url, example_question, groq_api_key)
#     print(answer)

