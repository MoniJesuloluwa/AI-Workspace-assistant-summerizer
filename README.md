# 🧠 AI File & Workspace Assistant

A Python-powered assistant that indexes, summarizes, and manages files in your local workspace using AI.  
It scans folders, extracts text from documents, saves key metadata in a database, and generates concise summaries using OpenAI’s GPT models.

---

## 🚀 Features

### 🗂️ Smart File Indexing
- Recursively scans directories
- Extracts text from `.txt`, `.md`, `.py`, `.json`, `.csv`, `.pdf`, and `.docx` files
- Stores all metadata (size, modified date, content, etc.) in a local SQLite database

### 🤖 AI-Powered Summarization
- Uses OpenAI’s API to generate 3–5 bullet-point summaries
- Helps you understand files at a glance without opening them

### 🔍 Fast Search
- Search across file names, summaries, or content
- Returns results instantly in a clean table view

### 💻 Command-Line Interface
Simple, human-readable commands:

```bash
python main.py index --path /your/folder
python main.py list
python main.py search --q "invoice"
python main.py summarize --limit 5
🧩 Project Structure
csharp
Copy code
ai_workspace_assistant/
│
├── core/
│   ├── ai_agent.py           # Handles OpenAI communication
│   ├── file_analyzer.py      # Extracts text from supported file types
│   └── workspace_manager.py  # Manages SQLite database
│
├── ui/
│   └── cli.py                # Command-line interface logic
│
├── data/
│   └── workspace.db          # Auto-created database
│
├── main.py
├── requirements.txt
├── .env.example
└── README.md
⚙️ Installation
1️⃣ Set up your environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate
2️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Add your API key
Create a .env file:

ini
Copy code
OPENAI_API_KEY=api-key
OPENAI_MODEL=gpt-4o-mini
🧠 Example Usage
Index a folder
bash
Copy code
python main.py index --path data/sample_texts
Generate summaries
bash
Copy code
python main.py summarize --limit 5
List all files
bash
Copy code
python main.py list
Search for files
bash
Copy code
python main.py search --q "AI"
🛠️ Technologies Used
Python 3.11+

OpenAI API

Rich for terminal UI

SQLite for metadata storage

PyPDF2 and python-docx for text extraction

🌟 Future Enhancements
AI file categorization

GUI dashboard (Streamlit)

Duplicate detection and cleanup

Context-aware organization suggestions