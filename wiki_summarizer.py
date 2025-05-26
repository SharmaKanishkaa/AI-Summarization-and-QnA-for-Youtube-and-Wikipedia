import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Used to rank sentences according sentence scores
from heapq import nlargest
from scraper import scraper
import spacy
from heapq import nlargest

def summarizer(text):
    '''Summarizes text by tokenizing, creating a word frequency list, 
        finding sentence scores, and then selecting sentences with 
        highest sentence scores'''

    stopwords = list(STOP_WORDS)

    # Load spaCy model for tokenization
    nlp = spacy.load('en_core_web_sm')

    # Tokenize the text
    doc = nlp(text)

    # Calculate word frequencies
    word_frequencies = {}
    for word in doc:
        # Ensure `word` is not punctuation and is not in stopwords
        if word.text.lower() not in stopwords and word.text not in punctuation:
            if word.text.lower() not in word_frequencies:
                word_frequencies[word.text.lower()] = 1
            else:
                word_frequencies[word.text.lower()] += 1

    # Normalize frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency

    # Tokenize sentences and calculate sentence scores
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if sent not in sentence_scores:
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Select top sentences for the summary
    select_count = int(len(sentence_tokens) * 0.2)
    summary_sentences = nlargest(select_count, sentence_scores, key=sentence_scores.get)
    summary = " ".join([sent.text for sent in summary_sentences])

    return summary

