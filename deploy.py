import streamlit as st
from fetch_transcript import fetch_transcript
from summarizer import summarize_with_bart, summarize_with_t5
from scraper import scraper
from wiki_summarizer import summarizer
from youtube_qa import youtube_qa_system
from wiki_qa import content_qa_system
from question_generation_main import QuestionGeneration

# Set page config
st.set_page_config(
    page_title="Note AI",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }
    .main-heading {
        text-align: center;
        color: #ffffff;
        text-shadow: 1px 1px 4px #000;
    }
    .sub-heading {
        text-align: center;
        margin-top: -10px;
        color: #f7f7f7;
    }
    .custom-icon {
        font-size: 50px;
        text-align: center;
        margin: 10px 0;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        box-shadow: 2px 2px 5px #888888;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-heading'>Note AI - Summarization Tools</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-heading'>Simplify information extraction with YouTube and Wikipedia tools</p>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Menu")
options = ["Home", "YouTube Tools", "Wikipedia Tools"]
choice = st.sidebar.radio("Choose an option:", options)

# Home Page
if choice == "Home":
    st.markdown("### Welcome to Note AI - Summarization Tools!")
    st.markdown("""
        Use this tool to:
        - Summarize YouTube videos or answer questions based on their content.
        - Extract and summarize content from Wikipedia articles.
    """)

# YouTube Tools Page
elif choice == "YouTube Tools":
    st.markdown("<h2 class='custom-icon'>📺 YouTube Tools</h2>", unsafe_allow_html=True)

    sub_options = ["Summarizer", "Q&A", "Question Generation"]
    yt_choice = st.selectbox("Choose a tool:", sub_options)

    if yt_choice == "Summarizer":
        st.markdown("### YouTube Video Summarizer")
        yt_url = st.text_input("Enter YouTube video URL:")
        if st.button("Generate Summary"):
            if yt_url:
                try:
                    transcript = fetch_transcript(yt_url)
                    summary = summarize_with_bart(transcript)
                    st.text_area("Transcript Summary:", summary, height=200)
                except Exception as e:
                    st.error(f"The YouTube Video URL provided does not contain a transcript. {str(e)}")

    elif yt_choice == "Q&A":
        st.markdown("### YouTube Video Q&A")
        yt_url = st.text_input("Enter YouTube video URL:")
        question = st.text_area("Enter your question:")
        if st.button("Get Answer"):
            if yt_url and question:
                try:
                    groq_api_key = "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"
                    answer = youtube_qa_system(yt_url, question, groq_api_key)
                    st.text_area("Answer:", answer, height=200)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    elif yt_choice == "Question Generation":
        st.markdown("### YouTube Video Question Generation")
        yt_url = st.text_input("Enter YouTube video URL:")
        num_questions = st.selectbox("Select number of questions to generate:", [5, 10, 15, 20])
        if st.button("Generate Questions"):
            if yt_url:
                try:
                    transcript = fetch_transcript(yt_url)
                    summary = summarize_with_bart(transcript)
                    st.text_area("Transcript Summary:", summary, height=200)

                    question_generator = QuestionGeneration(num_questions, 4)
                    questions = question_generator.generate_questions_dict(summary)

                    for i, q in questions.items():
                        with st.expander(f"Q{i}: {q['question']}"):
                            for key, op in sorted(q['options'].items()):
                                st.markdown(f"**Option {key}:** {op}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Wikipedia Tools Page
elif choice == "Wikipedia Tools":
    st.markdown("<h2 class='custom-icon'>🌐 Wikipedia Tools</h2>", unsafe_allow_html=True)

    sub_options = ["Summarizer", "Q&A", "Question Generation"]
    wiki_choice = st.selectbox("Choose a tool:", sub_options)

    if wiki_choice == "Summarizer":
        st.markdown("### Wikipedia Article Summarizer")
        wiki_url = st.text_input("Enter Wikipedia article URL:")
        if st.button("Generate Summary"):
            if wiki_url:
                try:
                    _, content = scraper(wiki_url)
                    summary = summarizer(content)
                    st.text_area("Article Summary:", summary, height=200)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    elif wiki_choice == "Q&A":
        st.markdown("### Wikipedia Article Q&A")
        wiki_url = st.text_input("Enter Wikipedia article URL:")
        question = st.text_area("Enter your question:")
        if st.button("Get Answer"):
            if wiki_url and question:
                try:
                    groq_api_key = "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"
                    answer = content_qa_system(wiki_url, question, groq_api_key)
                    st.text_area("Answer:", answer, height=200)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    elif wiki_choice == "Question Generation":
        st.markdown("### Wikipedia Article Question Generation")
        wiki_url = st.text_input("Enter Wikipedia article URL:")
        num_questions = st.selectbox("Select number of questions to generate:", [5, 10, 15, 20])
        if st.button("Generate Questions"):
            if wiki_url:
                try:
                    _, content = scraper(wiki_url)
                    summary = summarizer(content)
                    st.text_area("Article Summary:", summary, height=200)

                    question_generator = QuestionGeneration(num_questions, 4)
                    questions = question_generator.generate_questions_dict(summary)

                    for i, q in questions.items():
                        with st.expander(f"Q{i}: {q['question']}"):
                            for key, op in sorted(q['options'].items()):
                                st.markdown(f"**Option {key}:** {op}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
