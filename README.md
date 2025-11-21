📚 Multi‑Region Cybersecurity Chatbot
A local, privacy‑first AI assistant that answers cybersecurity questions using only official government sources from Hong Kong, Japan, and New York City. The system combines a Retrieval‑Augmented Generation (RAG) pipeline with a local Ollama LLM (Llama 3.2), guaranteeing source‑attributed answers and zero hallucinations—all without any cloud API keys.

✨ Key Features
Multi‑region support – query HK, JP, NYC or all regions at once.
Strict source attribution – every fact is cited with clickable links and region tags.
Local inference with Ollama – no external API, zero cost, full data privacy.
Dynamic UI – dark Gemini‑style theme with region‑specific colors and smooth micro‑animations.
Glass‑morphism design – premium look and feel that wows at first glance.
Extensible architecture – add new government portals by creating a Scrapy spider.
🛠️ Tech Stack
Layer	Technology
Backend	FastAPI, Uvicorn, Python 3.13
Vector Store	ChromaDB (local)
Embedding Model	all‑MiniLM‑L6‑v2 (SentenceTransformers)
LLM	Ollama + Llama 3.2 (local)
RAG Framework	LangChain
Web Scraping	Scrapy
Frontend	React 18 + Vite, vanilla CSS, Lucide icons
Styling	Inter font, glass‑morphism, gradient background, dark theme
Environment	
.env
 for config (no API keys needed)
🚀 Quick Start
bash
# 1️⃣ Clone the repo
git clone <repo‑url>
cd Chatbot

# 2️⃣ Backend setup
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python ingest.py          # load the 42 government documents into ChromaDB
python main.py            # start FastAPI (http://localhost:8000)

# 3️⃣ Frontend setup
cd ../frontend
npm install
npm run dev               # opens http://localhost:5173

# 4️⃣ Ollama model (run once)
ollama pull llama3.2
The UI will load automatically; select a region and ask any cybersecurity question.

📖 Usage Example
json
POST /query
{
  "query": "What is ransomware?",
  "region": "HK"
}
Response

json
{
  "answer": "Ransomware is malicious software that encrypts files and demands payment [1][2].",
  "sources": [
    {
      "title": "Protect Yourself against Ransomware",
      "url": "https://www.cybersecurity.hk/.../ransomware",
      "region": "HK"
    },
    {
      "title": "Beware of Phishing Attacks",
      "url": "https://www.cybersecurity.hk/.../phishing",
      "region": "HK"
    }
  ]
}
📂 Repository Structure
Chatbot/
├─ backend/            # FastAPI, RAG pipeline, Scrapy spiders
│   ├─ crawler/
│   ├─ chroma_db/      # local vector store (git‑ignored)
│   ├─ ingest.py
│   ├─ main.py
│   └─ requirements.txt
├─ frontend/
│   ├─ src/
│   │   ├─ App.jsx
│   │   └─ index.css
│   └─ package.json
├─ design/             # architecture & docs
├─ .gitignore
├─ .env                # only OLLAMA_KEY (placeholder)
└─ README.md           # ← this file
🤝 Contributing
Fork the repo.
Create a feature branch (git checkout -b feature/awesome‑thing).
Add your code, run the existing tests, and ensure the UI still works.
Submit a Pull Request with a clear description of the change.
Feel free to add new government portals by creating a Scrapy spider in backend/crawler/spiders/ and updating ingest.py.

📄 License
This project is released under the MIT License – you’re free to use, modify, and distribute it.

🙏 Acknowledgments
Ollama for providing a fast, local LLM runtime.
LangChain for simplifying the RAG workflow.
ChromaDB for an easy‑to‑use vector store.
The government portals (HK, NISC, NYC OTI) for open, authoritative cybersecurity information.
