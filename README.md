# Personalized Networking Assistant

Personalized Networking Assistant is a professional-grade, AI-powered system designed to generate tailored conversation starters and verify networking topics in real-time. Built using **FastAPI** for high-performance REST endpoints and **Streamlit** for a modern, glassmorphic UI, it employs state-of-the-art NLP models (HuggingFace Zero-Shot and GPT-2) alongside the Wikipedia API for factual checks.

---

## 📂 Project Structure

```text
PersonalizedNetworkingAssistant/
├── app/
│   ├── __init__.py
│   ├── config.py             # Configuration and environment loaders
│   ├── main.py               # FastAPI server entry point and middlewares
│   ├── schemas.py            # Pydantic data schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── conversation.py   # REST API endpoint routers
│   └── services/
│       ├── __init__.py
│       ├── event_analyzer.py # Zero-Shot event theme extraction
│       ├── topic_generator.py# GPT-2 / template-based starter generation
│       ├── fact_checker.py   # Wikipedia-based topic verification
│       ├── history_logger.py # Local JSON session tracking
│       └── feedback_logger.py# Local JSON rating logger
├── frontend/
│   └── streamlit_app.py      # Streamlit glassmorphic dashboard
├── tests/
│   ├── conftest.py           # Pytest shared environment path configurations
│   ├── test_event.py         # Unit tests for event analyzer
│   ├── test_generator.py     # Unit tests for topic generator
│   ├── test_factchecker.py   # Unit tests for fact-checker (mocked)
│   └── test_routes.py        # Integration tests for FastAPI endpoints
├── .env                      # Loaded environment config
├── .env.example              # Environment variables template
├── history.json              # Persistent session store
├── feedback.json             # Persistent feedback ratings store
├── requirements.txt          # Python packaging dependencies
└── README.md                 # Project guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.11** installed on your system.

### 2. Environment Setup

Clone or place the project directory inside your preferred environment, then create and activate a Python virtual environment:

#### Windows (Command Prompt or PowerShell)
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installation
Install all required libraries pinned in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Copy `.env.example` to `.env` (it will be loaded automatically):
```bash
cp .env.example .env
```

---

## ⚙️ Running the Application

This application consists of two components running concurrently:

### Step A: Run the Backend
Start the FastAPI REST backend server using `uvicorn`:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **API Server Endpoint**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Step B: Run the Frontend
In a new terminal window (with the virtual environment activated), start the Streamlit UI dashboard:
```bash
streamlit run frontend/streamlit_app.py
```
- **Frontend Dashboard**: [http://localhost:8501](http://localhost:8501)

---

## 🧪 Testing

To run the automated test suite, make sure you are in the project root directory and execute:
```bash
pytest -v
```

This runs all tests inside the `tests/` directory:
1. **Event Analyzer**: Validates themes classification contracts.
2. **Conversation Generator**: Tests generation output formatting.
3. **Fact Checker**: Validates mocked Wikipedia API calls.
4. **API Routes**: Asserts FastAPI endpoint status codes and responses.

---

## 💡 Key Features
- **Zero-Shot Theme Classification**: Automatically extracts the most relevant themes from event descriptions.
- **Hybrid AI Generation**: Leverages GPT-2 text-generation alongside highly-tuned fallback templates to deliver 5 natural conversation starters.
- **Wikipedia Fact Checker**: Instantly verifies terms, showing verification status, URLs, and summaries.
- **Local Persistence & Feedback Loop**: Keeps full logs of generation sessions and user ratings for continuous improvement.
