# 💹 Financial News Intelligence Agent

Stay ahead of the markets — intelligently.

This Streamlit-based application is a comprehensive financial intelligence tool. It fetches live news headlines, provides near-instant summaries using the high-speed Groq API (with Llama 3), analyzes sentiment, extracts key entities, and features an interactive financial chatbot to answer your questions.

---

## 🚀 Features

- 📰 **Live Financial News Feed** — powered by [NewsAPI](https://newsapi.org/)
- 🧠 **AI Summarization** — Uses the Groq API with Llama 3 to generate customizable-length summaries almost instantly generates
- 💬 **Interactive Financial Chatbot** - Ask questions about markets, economics, or financial concepts and get instant answers from the AI.
- 😊 **Sentiment Analysis** — TextBlob shows how positive, negative, or neutral each article is
- 🏷️ **Named Entity Recognition** — highlights key financial entities (ORG, MONEY, GPE, etc.)
- 🔍 **Keyword Filtering** — instantly find relevant articles
- 🎛️ **Customizable Summary Length** — choose between Very Short to Long summaries

---

## 🛠️ Tech Stack

| Category             | Tools Used                          |
| -------------------- | ----------------------------------- |
| 🧠 Language Model    | Llama 3 (via Groq API)              |
| 🔍 Summarization     | LangChain + langchain-groq.         |
| 🌐 News API          | [NewsAPI.org](https://newsapi.org/) |
| 💬 Sentiment         | TextBlob                            |
| 🧾 Entity Extraction | spaCy (NER with `en_core_web_sm`)   |
| 🎨 UI Framework      | Streamlit                           |

---

## 🧑‍💻 Local Setup

### 1. Clone the Repository

git clone https://github.com/yourusername/FinSage.git
cd FinSage

### 2. Set Up a Virtual Environment

python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 4. Add Environment Variables

Create a `.env` file in the root directory and add your NewsAPI key:

NEWSAPI_KEY=your_newsapi_key_here
GROQ_API_KEY="gsk_your_groq_api_key_here"

### 5. Launch the Streamlit App

streamlit run app.py

---

## 🛠️ Optional Tips

- For better Streamlit performance, install the file watcher:

pip install watchdog

- Customize summary lengths and filters easily from the sidebar UI.

---

## 📄 License

MIT License © Sarthak Sukhral

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests for improvements or bug fixes.

---

## 🙏 Acknowledgements

- [NewsAPI](https://newsapi.org/) for financial news data
- [Ollama](https://ollama.com/) and [Mistral](https://mistral.ai/) for local LLM capabilities
- [LangChain](https://github.com/hwchase17/langchain) for LLM integration
- [Streamlit](https://streamlit.io/) for app framework
- [spaCy](https://spacy.io/) for entity extraction

---
