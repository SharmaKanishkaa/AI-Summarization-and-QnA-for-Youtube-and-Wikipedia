# NoteAI: Summarization, Q\&A, and Quiz Generator for YouTube and Wikipedia

**NoteAI** is an open-source, AI-powered educational assistant that simplifies complex learning content from YouTube videos and Wikipedia articles. Built using **Python** and **Streamlit**, it integrates cutting-edge Natural Language Processing (NLP) technologies to offer a user-friendly interface for summarization, intelligent question answering, and dynamic quiz generation.
**This tool is part of a research study published in 2nd International Conference on Computational Science, Communication Technology & Networking (CICTN 2025).**
> You can access the full paper here: [**Read the Research Paper**](https://ieeexplore.ieee.org/document/10932550)

### Workflow Diagrams

- **Application Overview**  
  ![Workflow Diagram of the Application](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/flowchart.png)

---

## Features

* **YouTube Transcript Summarization:** Automatically fetches and summarizes transcripts from YouTube videos.
* **Wikipedia Article Summarization:** Retrieves and condenses long Wikipedia articles into concise, coherent summaries.
* **AI-Powered Q\&A:** Contextual question-answering using LLaMA 3.1 via the Groq API for both YouTube and Wikipedia content.
* **Dynamic Quiz Generation:** Generates multiple-choice quizzes using spaCy’s NER and TF-IDF scoring.
* **Modular Architecture:** Each component (summarization, Q\&A, quiz) functions independently for maximum flexibility.
* **Interactive Streamlit UI:** Clean and intuitive web interface for easy navigation and usage.

---
## 📸 Visual Overview

| Home Page | YouTube Summarization Tool | YouTube Q&A Tool |
|-----------|-----------------------------|-------------------|
| ![Home](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/homepage.png) | ![YouTube Summarizer](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/summarizer%201.png) | ![YouTube QnA](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/q%26a.png) |

| Wikipedia Summarization Tool | Wikipedia Q&A Tool |
|------------------------------|---------------------|
| ![Wikipedia Summarizer](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/summarizer.png) | ![Wikipedia QnA](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/q%26a%201.png) |

---

## Why NoteAI?

Students and independent learners often face:

* **Information Overload** from lengthy educational content.
* **Time-Consuming Manual Notes** and ineffective study methods.
* **Lack of Interactivity** in traditional study formats.
* **Poor Retention** due to absence of revision tools like quizzes or flashcards.

**NoteAI** addresses these challenges by:

* Summarizing content into digestible formats.
* Enabling real-time interaction with material through Q\&A.
* Reinforcing learning with automatically generated quizzes.

---
 - **Summarization Module**  
  ![Workflow of Summarization Module](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/workflow.png)

- **Q&A Module**  
  ![Workflow of QnA Module](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/workflow1.png)

- **Quiz Generation Module**  
  ![Workflow of Quiz Generation Module](https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia/blob/main/workflow2.png)

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (with custom CSS)
* **Backend:** Python
* **NLP Models:**

  * [PEGASUS](https://huggingface.co/google/pegasus) – Abstractive Summarization
  * [LLaMA 3.1](https://huggingface.co/meta-llama) via Groq API – Contextual Q\&A
  * spaCy – Named Entity Recognition
  * TF-IDF – Keyword and distractor ranking
* **External Libraries/APIs:**

  * `youtube_transcript_api` – YouTube transcript extraction
  * `wikipedia`, `BeautifulSoup` – Wikipedia content parsing

---

## Core Modules

### 1. YouTube Module

* **Transcript Retrieval:** Extracts video transcript using YouTube API or `youtube_transcript_api`.
* **Summarization:** Chunked summarization using PEGASUS with context continuity.
* **Q\&A:** Accepts user queries and returns accurate responses using LLaMA 3.1 via Groq API.

### 2. Wikipedia Module

* **Content Fetching:** Retrieves and cleans text from article URLs or titles using `wikipedia` and `BeautifulSoup`.
* **Summarization:** Section-wise summarization using BART/T5.
* **Q\&A:** Contextual response generation using LLaMA 3.1.

### 3. Quiz Generator

* **Named Entity Extraction:** Key concepts extracted using spaCy’s NER.
* **Distractor Selection:** Distractors generated using TF-IDF relevance scoring.
* **Question Format:** Each question includes 1 correct option + 3 plausible distractors.

---

## Functional Requirements

### Input Capabilities

* YouTube URL input
* Wikipedia article title or URL
* Optional user questions
* Desired number of quiz questions

### Output Capabilities

* Summarized content
* Context-aware answers
* Multiple-choice quizzes

### User Interface

* Clean navigation sidebar
* Module-specific input fields and results display
* Instant feedback and result rendering

---

## Experimental Evaluation

An experimental evaluation was conducted to test:

* **Summary Quality** – Evaluated for conciseness, coherence, and informativeness.
* **Q\&A Accuracy** – Validated against known content points.
* **Quiz Relevance** – Tested on domain-specific articles for distractor and concept validity.

Though formal metrics like ROUGE or BLEU were not employed, qualitative assessments confirmed high-quality outputs across domains including education, science, and technology.

---

## Project Structure

```
NoteAI/
│
├── app.py                   # Streamlit main app file
├── utils/
│   ├── summarizer.py        # Summarization functions (PEGASUS, BART, etc.)
│   ├── qna.py               # Q&A interface using LLaMA 3.1 (Groq API)
│   ├── quiz_generator.py    # NER + TF-IDF-based MCQ generator
│   ├── youtube_utils.py     # YouTube transcript extraction
│   └── wiki_utils.py        # Wikipedia parsing and cleaning
├── requirements.txt
├── README.md
└── assets/                  # Styling or example inputs
```

---

## Installation & Setup

### Prerequisites

* Python 3.8+
* Groq API key for LLaMA-3.1 Q\&A

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/SharmaKanishkaa/AI-Summarization-and-QnA-for-Youtube-and-Wikipedia.git
cd AI-Summarization-and-QnA-for-Youtube-and-Wikipedia

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key as an environment variable
export GROQ_API_KEY="your_api_key_here"  # Or use dotenv

# Run the app
streamlit run app.py
```
## Future Improvements

* Flashcard integration (e.g., via Anki)
* ROUGE-based summary evaluation
* Support for PDF/HTML/Book content
* Personalized learning paths based on quiz performance
* Voice-to-text transcript ingestion

---

## Contact

For feedback, issues, or collaboration opportunities, reach out via:

* **Email:** [Kanishka Sharma Mail](mailto:sharmakanishka1604@gmail.com)
* **LinkedIn:** [LinkedIn Profile](www.linkedin.com/in/sharma-kanishka16)

