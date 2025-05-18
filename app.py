import streamlit as st
import requests
from textblob import TextBlob
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import spacy

nlp = spacy.load("en_core_web_sm")

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def fetch_news(api_key, page_size=20):
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category=business&language=en&pageSize={page_size}&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return articles
    except requests.HTTPError as e:
        st.error(f"Error fetching news: {e}")
        return []


def load_llm():
    return Ollama(model="mistral")


@st.cache_data(show_spinner=False)
def summarize_text(text, length_label="Short"):
    prompt_templates = {
        "Very Short": "Summarize this financial news article in 1 sentence:\n{text}",
        "Short": "Summarize this financial news article briefly in 2-3 sentences:\n{text}",
        "Medium": "Provide a concise summary of this financial news article in 4-5 sentences:\n{text}",
        "Long": "Write a detailed summary of this financial news article:\n{text}",
    }
    prompt = PromptTemplate.from_template(prompt_templates[length_label])
    llm = load_llm()
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(text=text)



def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive 😊", "green"
    elif polarity < -0.1:
        return "Negative 😞", "red"
    else:
        return "Neutral 😐", "gray"

def extract_financial_entities(text):
    doc = nlp(text)
    entities = set()
    for ent in doc.ents:
        if ent.label_ in ("ORG", "GPE", "MONEY", "PRODUCT", "PERSON"):
            entities.add(ent.text)
    return list(entities)

def main():
    st.set_page_config(page_title="Financial News Intelligence Agent", page_icon="📉",layout="wide")
    st.title("📉 Financial News Intelligence Agent")
    st.markdown("""
        <style>
            .description {
                font-size: 1.1rem;
                color: #444;
                margin-bottom: 2rem;
            }
            .entity-badge {
                background-color: #dbeafe;
                color: #1e40af;
                padding: 5px 10px;
                margin: 3px 4px 3px 0;
                border-radius: 10px;
                font-size: 0.85rem;
                display: inline-block;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(
        '<p class="description"> Stay updated effortlessly — browse, summarize, and analyze the latest financial news with local AI-powered summaries and sentiment insights.</p>',
        unsafe_allow_html=True)

    if NEWSAPI_KEY is None:
        st.error("Please set your NEWSAPI_KEY in the .env file")
        return

    # Sidebar filters
    st.sidebar.header("Filters & Settings")
    st.sidebar.markdown(
        """
         **Customize your financial news feed:**

        - **Number of Articles**: Choose how many articles to fetch.
        - **Keyword Filter**: Narrow down results by topic.
        - **Summary Length**: Decide how detailed the AI summaries should be.
        """
    )

    max_articles = st.sidebar.slider("Number of articles to fetch", 5, 20, 10)
    keyword_filter = st.sidebar.text_input("Filter articles by keyword")

    with st.spinner("Fetching latest news..."):
        articles = fetch_news(NEWSAPI_KEY, page_size=max_articles)

    if keyword_filter:
        articles = [
            art for art in articles if keyword_filter.lower() in (art.get("title") or "").lower()
            or keyword_filter.lower() in (art.get("description") or "").lower()
        ]

    if not articles:
        st.warning("No articles found with the given criteria.")
        return

    summary_length = st.sidebar.selectbox(
        "Summary length",
        options=["Very Short", "Short", "Medium", "Long"],
        index=1,
        help="Choose how detailed the article summaries should be."
    )

    llm = load_llm()  # Load once for performance

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No Title")
        description = article.get("description") or title
        url = article.get("url", "#")
        source = article.get("source", {}).get("name", "Unknown Source")

        with st.expander(f"{i}. {title} ({source})"):
            st.write(description)

            entities = extract_financial_entities(description)
            if entities:
                st.markdown(
                    "🔖 **Key Entities:** " +
                    " ".join([f'<span class="entity-badge">{ent}</span>' for ent in entities]),
                    unsafe_allow_html=True
                )

            with st.spinner("Summarizing article..."):
                summary = summarize_text(description, length_label=summary_length)

            # Use columns for summary, sentiment, and link
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown(f"**Summary:** {summary}")

            with col2:
                sentiment_text, sentiment_color = analyze_sentiment(description)
                st.markdown(f"**Sentiment:**")
                st.markdown(f"<span style='color:{sentiment_color};font-weight:bold'>{sentiment_text}</span>",
                            unsafe_allow_html=True)

            with col3:
                st.markdown(f"[Read full article]({url})")

            st.markdown("---")

if __name__ == "__main__":
    main()
