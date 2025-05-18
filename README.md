# 💹 Financial News Intelligence Agent

Stay ahead of the markets — intelligently.

This Streamlit-based app fetches the latest financial headlines, summarizes them using a **local LLM (Mistral via Ollama)**, extracts key financial entities, and analyzes sentiment — giving you a fast, AI-powered overview of the financial world.

---

## 🚀 Features

- 📰 **Live Financial News Feed** — powered by [NewsAPI](https://newsapi.org/)
- 🧠 **AI Summarization** — local LLM (Mistral via Ollama) generates customizable-length summaries
- 😊 **Sentiment Analysis** — TextBlob shows how positive, negative, or neutral each article is
- 🏷️ **Named Entity Recognition** — highlights key financial entities (ORG, MONEY, GPE, etc.)
- 🔍 **Keyword Filtering** — instantly find relevant articles
- 🎛️ **Customizable Summary Length** — choose between Very Short to Long summaries

---

## 🛠️ Tech Stack

| Category            | Tools Used                               |
|---------------------|-------------------------------------------|
| 🧠 Language Model    | Mistral (via [Ollama](https://ollama.com/)) |
| 🔍 Summarization     | LangChain + PromptTemplate + Ollama       |
| 🌐 News API          | [NewsAPI.org](https://newsapi.org/)       |
| 💬 Sentiment         | TextBlob                                  |
| 🧾 Entity Extraction | spaCy (NER with `en_core_web_sm`)         |
| 🎨 UI Framework      | Streamlit                                 |

---

## 🧑‍💻 Local Setup

> ⚠️ Requires Ollama installed and Mistral model pulled locally.

### 1. Clone the Repository

git clone https://github.com/yourusername/FinSage.git
cd FinSage

### 2. Set Up a Virtual Environment

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 4. Add Environment Variables

Create a `.env` file in the root directory and add your NewsAPI key:

NEWSAPI_KEY=your_newsapi_key_here

### 5. Ensure Mistral is Available in Ollama

Make sure Ollama is installed and the Mistral model is running locally:

ollama run mistral

> The app uses LangChain with the local `mistral` model served via Ollama.

### 6. Launch the Streamlit App

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

