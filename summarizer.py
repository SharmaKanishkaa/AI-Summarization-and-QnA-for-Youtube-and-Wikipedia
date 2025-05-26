from fetch_transcript import fetch_transcript, preprocess_transcript
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, BartForConditionalGeneration, BartTokenizer, T5ForConditionalGeneration, T5Tokenizer

# Splitting Text into Chunks
def split_into_chunks(text, chunk_size=400):
    """
    Splits input text into smaller chunks of a defined size.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

# Summarization with Chunking
def summarize_with_chunks(text, model_name, tokenizer_class, model_class, chunk_size=400):
    """
    Summarizes long text by splitting it into chunks and summarizing each chunk.
    
    Args:
        text (str): Input text to summarize.
        model_name (str): Pretrained model name.
        tokenizer_class: Tokenizer class for the model.
        model_class: Model class for summarization.
        chunk_size (int): Maximum number of words per chunk.

    Returns:
        str: Combined summary from all chunks.
    """
    tokenizer = tokenizer_class.from_pretrained(model_name)
    model = model_class.from_pretrained(model_name)

    summaries = []
    for chunk in split_into_chunks(text, chunk_size):
        inputs = tokenizer(chunk, max_length=1024, truncation=True, return_tensors="pt")
        summary_ids = model.generate(
            inputs["input_ids"], max_length=80, min_length=20, length_penalty=2.0, num_beams=6
        )
        summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

    return " ".join(summaries)


    

# BART Summarization
def summarize_with_bart(text):
    return summarize_with_chunks(
        text, 
        model_name="facebook/bart-large-cnn", 
        tokenizer_class=BartTokenizer, 
        model_class=BartForConditionalGeneration
    )

# T5 Summarization
def summarize_with_t5(text):
    return summarize_with_chunks(
        text, 
        model_name="t5-small",  # Use "t5-base" or "t5-large" for better results
        tokenizer_class=T5Tokenizer, 
        model_class=T5ForConditionalGeneration,
        chunk_size=200  # T5 handles smaller chunks better
    )



















# from transformers import pipeline
# import spacy
# from spacy.lang.en.stop_words import STOP_WORDS
# from numpy import numpy.core.multiarray
# import re

# # def summarize_with_pegasus(text, chunk_size=512):
# #     # Load tokenizer and model
# #     tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
# #     model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

# #     # Split text into chunks
# #     words = text.split()
# #     chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# #     # Summarize each chunk
# #     summaries = []
# #     for chunk in chunks:
# #         tokens = tokenizer(chunk, truncation=True, padding="longest", return_tensors="pt")
# #         summary_ids = model.generate(
# #             tokens["input_ids"],
# #             max_length=100,
# #             min_length=30,
# #             length_penalty=2.0,
# #             num_beams=4,
# #         )
# #         summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

# #     # Combine summaries
# #     return " ".join(summaries)

# # def summarize(text):

# #     stopwords = list(STOP_WORDS)
# #     nlp = spacy.load('en_core_web_sm')
# #     doc = nlp(text)
# #     tokens = [token.text for token in doc]
# #     # Initialize summarization pipelines
# #     pegasus_summarizer = pipeline('summarization', model='google/pegasus-xsum')
# #     bart_summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
# #     t5_summarizer = pipeline('summarization', model='t5-small')

# #     def summarize_with_model(text, summarizer, max_length=150, min_length=50):
# #         return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

# #     # Example usage
# #     pegasus_summary = summarize_with_model(text, pegasus_summarizer)
# #     bart_summary = summarize_with_model(text, bart_summarizer)
# #     t5_summary = summarize_with_model(text, t5_summarizer)

# #     print("Pegasus Summary:", pegasus_summary)
# #     print("BART Summary:", bart_summary)
# #     print("T5 Summary:", t5_summary)

# from fetch_transcript import fetch_transcript, preprocess_transcript
# from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# def summarize_with_pegasus(transcript: str, chunk_size: int = 200):
#     """
#     Summarize the given transcript using the Pegasus model.

#     Args:
#         transcript: The input transcript text.
#         chunk_size: Maximum size of each chunk for summarization.

#     Returns:
#         str: The summarized text.
#     """
#     tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
#     model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

#     # Preprocess transcript into chunks
#     chunks = preprocess_transcript(transcript, chunk_size)

#     # Summarize each chunk
#     summaries = []
#     for chunk in chunks:
#         tokens = tokenizer(chunk, truncation=True, padding="longest", return_tensors="pt")
#         summary_ids = model.generate(
#             tokens["input_ids"],
#             max_length=100,
#             min_length=30,
#             length_penalty=2.0,
#             num_beams=4,
#         )
#         summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

#     # Combine summaries
#     return " ".join(summaries)

# if __name__ == "__main__":
#     # Example usage
#     video_url = "https://www.youtube.com/watch?v=81bCbEcB2qI"  # Replace with your video URL
#     transcript = fetch_transcript(video_url)

#     if transcript:
#         print("Transcript fetched successfully!")
#         print("\nGenerating summary...\n")
#         summarized_text = summarize_with_pegasus(transcript)
#         print("Summary:")
#         print(summarized_text)
#     else:
#         print("Failed to fetch the transcript.")



# # from fetch_transcript import fetch_transcript
# # from transformers import PegasusForConditionalGeneration, PegasusTokenizer
# # from rouge_score import rouge_scorer
# # from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
# # import nltk

# # # Ensure required nltk data is downloaded
# # nltk.download('punkt')

# # def summarize_with_pegasus(text, chunk_size=512):
# #     """
# #     Summarize the given text using the Pegasus model.
# #     Splits the text into chunks to handle model input size limitations.
# #     """
# #     tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
# #     model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

# #     # Split text into chunks
# #     words = text.split()
# #     chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# #     summaries = []
# #     for chunk in chunks:
# #         tokens = tokenizer(chunk, truncation=True, padding="longest", return_tensors="pt")
# #         summary_ids = model.generate(
# #             tokens["input_ids"],
# #             max_length=100,
# #             min_length=30,
# #             length_penalty=2.0,
# #             num_beams=4,
# #         )
# #         summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

# #     return " ".join(summaries)

# # def compute_rouge(reference, candidate):
# #     """
# #     Compute ROUGE-1 and ROUGE-L scores between reference and candidate summaries.
# #     """
# #     scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
# #     scores = scorer.score(reference, candidate)
# #     return scores

# # def compute_bleu(reference, candidate):
# #     """
# #     Compute BLEU score between reference and candidate summaries.
# #     """
# #     reference_tokens = reference.split()
# #     candidate_tokens = candidate.split()
# #     smoothing = SmoothingFunction().method1
# #     bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing)
# #     return bleu_score

# # if __name__ == "__main__":
# #     # Fetch transcript from video URL
# #     video_url = "https://www.youtube.com/watch?v=81bCbEcB2qI"  # Replace with your video URL
# #     transcript = fetch_transcript(video_url)

# #     if transcript:
# #         print("Transcript fetched successfully!")

# #         # Generate summary
# #         print("\nGenerating summaries...\n")
# #         candidate_summary = summarize_with_pegasus(transcript)
# #         print("Generated Summary:")
# #         print(candidate_summary)

# #         # Define a reference summary for evaluation
# #         reference_summary = (
# #             "My love affair with the table began when I was just nine years old. It might seem unusual, but let me explain. One day, while our parents were away, my siblings, cousins, and I were left alone at home. My older brother invited his friends over, and chaos ensued. During their antics, they broke my mother's cherished dining table, the centerpiece of our daily meals and celebrations. To cover it up, my brother used my jump rope to fix the table, but during dinner, it dramatically collapsed. That incident made me realize the profound role the table played in our lives. Without it, our family meals felt scattered and disconnected, highlighting how the table brought us together. This understanding deepened over time as I observed the table's significance in history and personal milestones—from ancient Egyptian rituals to negotiating peace treaties, to hosting joyful celebrations or navigating life’s challenges. I believe the table holds the power to foster connection, bridge divides, and preserve traditions. It’s a place to share stories, values, and moments that shape us. In today’s world, I strive to bring back its essence by cherishing shared meals, welcoming diverse voices, and modeling love and respect for the next generation. The table is not just furniture; it’s the heart of human connection."
# #         )

# #         # Compute ROUGE scores
# #         rouge_scores = compute_rouge(reference_summary, candidate_summary)
# #         print("\nROUGE Scores:")
# #         print(f"ROUGE-1: {rouge_scores['rouge1'].fmeasure:.4f}")
# #         print(f"ROUGE-L: {rouge_scores['rougeL'].fmeasure:.4f}")

# #         # Compute BLEU score
# #         bleu_score = compute_bleu(reference_summary, candidate_summary)
# #         print("\nBLEU Score:")
# #         print(f"BLEU: {bleu_score:.4f}")
# #     else:
# #         print("Failed to fetch the transcript.")

# from fetch_transcript import fetch_transcript, preprocess_transcript
# from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# def summarize_with_pegasus(transcript, chunk_size=512):
#     tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
#     model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

#     chunks = preprocess_transcript(transcript, chunk_size=chunk_size)
#     summaries = []
#     for chunk in chunks:
#         tokens = tokenizer(chunk, return_tensors="pt", truncation=True)
#         summary_ids = model.generate(tokens["input_ids"], max_length=100, num_beams=4)
#         summaries.append(tokenizer.decode(summary_ids[0], skip_special_tokens=True))

#     return " ".join(summaries)
