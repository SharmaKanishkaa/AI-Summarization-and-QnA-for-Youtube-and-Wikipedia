import bs4 as bs
import urllib.request
import re
from typing import List

def remove_brackets(text):
        '''Removes the citations and square brackets in super script from text'''
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        return re.sub(r'\s+', ' ', text)

def scraper(url):
    '''Scrapes content from paragraph and div tags of website'''
    article_text = ""

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(request)
    data = response.read()

    parsed_article = bs.BeautifulSoup(data, 'lxml')

    title = parsed_article.find('title').text

    paragraphs = parsed_article.find_all('p')

    # Checking content of p tags
    if len(paragraphs) != 0:
        for p in paragraphs:
            article_text += p.text
    
    # Checking content of div tags
    else:
        divs = parsed_article.find_all('div', id = 'container')

        for div in divs:
            article_text += div.text

    body = remove_brackets(article_text)
        
    return title, body


def preprocess_content(content: str, chunk_size: int = 200) -> List[str]:
    """
    Preprocess content into chunks with improved text splitting.
    Works for both Wikipedia and YouTube content.

    Args:
        content: Input text content
        chunk_size: Maximum size of each chunk

    Returns:
        List of text chunks
    """
    # Split on sentence boundaries
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', content) if s.strip()]
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
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

