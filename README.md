# 🤖 LinkedIn AI Content Agent

An intelligent agent that generates high-quality LinkedIn posts 
on Cybersecurity and AI topics — powered by GPT-4o and real-time 
web search.

## ✨ Features
- Real-time web research via Serper API
- Anti-hallucination: only uses verified facts
- Structured LinkedIn format (Hook → Insight → Twist → CTA)
- Auto-save generated posts
- Streamlit web interface

## 🛠️ Tech Stack
- Python 3.11+
- OpenAI GPT-4o
- Serper API (Google Search)
- Streamlit
- python-dotenv

## 🚀 Quick Start

# Clone the repo
git clone https://github.com/olade-sagbo/linkedin-ai-agent

# Install dependencies
pip install -r requirements.txt

# Add your API keys
cp .env.example .env
# Edit .env with your keys

# Run CLI agent
python agent.py

# Run web interface
streamlit run app.py

## 📁 Project Structure
linkedin-agent/
├── agent.py        # Core agent logic
├── researcher.py   # Web search module
├── prompts.py      # Prompt engineering
├── config.py       # Configuration
├── app.py          # Streamlit interface
└── posts/          # Saved generated posts

## 🔑 Environment Variables
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key

## 👤 Author
Olade Roland Sagbo — Cybersecurity & AI | Hamburg 🇩🇪
linkedin.com/in/olade-sagbo
