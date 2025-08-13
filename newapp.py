import streamlit as st
import requests
from textblob import TextBlob
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import spacy
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from chatbot import get_response 

nlp = spacy.load("en_core_web_sm")

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def fetch_news(api_key, page_size=20):
    """Fetches top business headlines from NewsAPI."""
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category=business&language=en&pageSize={page_size}&apiKey={api_key}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return articles
    except Exception as e:
        st.error(f"Error fetching news from NewsAPI: {e}")
        return []

@st.cache_resource(show_spinner="Loading AI Model...")
def load_llm():
    """Loads the Groq LLM. This is cached for efficiency."""
    if not GROQ_API_KEY:
        st.error("Groq API key not found. Please add GROQ_API_KEY to your .env file.")
        return None
    return ChatGroq(model_name="llama3-8b-8192", groq_api_key=GROQ_API_KEY, temperature=0.7)

@st.cache_data(show_spinner=False)
def summarize_text(_llm, text, length_label="Short"):
    """Summarizes a single piece of text using the provided LLM."""
    prompt_templates = {
        "Very Short": "Summarize this financial news article in 1 sentence:\n{text}",
        "Short": "Summarize this financial news article briefly in 2-3 sentences:\n{text}",
        "Medium": "Provide a concise summary of this financial news article in 4-5 sentences:\n{text}",
        "Long": "Write a detailed summary of this financial news article:\n{text}",
    }
    prompt = PromptTemplate.from_template(prompt_templates[length_label])
    output_parser = StrOutputParser()
    chain = prompt | _llm | output_parser
    return chain.invoke({"text": text})

def analyze_sentiment(text):
    """Analyzes the sentiment of a given text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive 😊", "green"
    elif polarity < -0.1:
        return "Negative 😞", "red"
    else:
        return "Neutral 😐", "gray"

def extract_financial_entities(text):
    """Extracts relevant financial entities from text using spaCy."""
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "GPE", "MONEY", "PRODUCT", "PERSON")]
    return list(set(entities))

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="FinSage", page_icon="📉", layout="wide")
    st.title("📉 Financial News Intelligence Agent")

    st.markdown("""
        <style>
            .description { font-size: 1.1rem; color: #444; margin-bottom: 2rem; }
            .entity-badge { background-color: #dbeafe; color: #1e40af; padding: 5px 10px; margin: 3px 4px 3px 0; border-radius: 10px; font-size: 0.85rem; display: inline-block; }
        </style>
    """, unsafe_allow_html=True)
    
    llm = load_llm()
    if llm is None:
        st.stop()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm your financial assistant. How can I help you today?"),
        ]

    tab1, tab2 = st.tabs(["📰 News Feed", "💬 Chatbot"])

    with tab1:
        st.sidebar.header("News Feed Settings")
        max_articles = st.sidebar.slider("Number of articles", 3, 15, 5)
        keyword_filter = st.sidebar.text_input("Filter news by keyword")
        summary_length = st.sidebar.selectbox("Summary length", ["Very Short", "Short", "Medium", "Long"], index=1)

        with st.spinner("Fetching latest news..."):
            articles = fetch_news(NEWSAPI_KEY, page_size=max_articles)

        if keyword_filter:
            articles = [art for art in articles if keyword_filter.lower() in (art.get("title") or "").lower() or keyword_filter.lower() in (art.get("description") or "").lower()]

        if not articles:
            st.warning("No articles found with the given criteria.")
        else:
            for article in articles:
                title = article.get("title", "No Title")
                description = article.get("description")
                url = article.get("url", "#")
                source = article.get("source", {}).get("name", "Unknown Source")
                content_to_process = description if description else title

                with st.expander(f"{title} ({source})"):
                    st.write(content_to_process)
                    
                    entities = extract_financial_entities(title + " " + (content_to_process or ""))
                    if entities:
                        st.markdown(
                            "🔖 **Key Entities:** " +
                            " ".join([f'<span class="entity-badge">{ent}</span>' for ent in entities]),
                            unsafe_allow_html=True
                        )
                    
                    summary = "Summary not available."
                    try:
                        with st.spinner("AI is summarizing..."):
                            summary = summarize_text(llm, content_to_process, length_label=summary_length)
                    except Exception as e:
                        st.warning(f"Could not generate summary: {e}")

                    col1, col2, col3 = st.columns([4, 1, 1])
                    with col1:
                        st.markdown(f"**Summary:** {summary}")
                    with col2:
                        sentiment, color = analyze_sentiment(content_to_process)
                        st.markdown(f"**Sentiment:** <span style='color:{color};font-weight:bold'>{sentiment}</span>", unsafe_allow_html=True)
                    with col3:
                        st.link_button("Read Article", url)

    with tab2:
        st.header("Financial Chatbot")
        
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)
        
        user_query = st.chat_input("Ask me about finance, markets, or economics...")
        if user_query:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            with st.chat_message("Human"):
                st.write(user_query)
            
            with st.chat_message("AI"):
                with st.spinner("Thinking..."):
                    response = get_response(user_query, st.session_state.chat_history, llm)
                    st.write(response)
                    st.session_state.chat_history.append(AIMessage(content=response))

if __name__ == "__main__":
    main()