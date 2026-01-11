# 🔬 ResearchAI: Autonomous Multi-Agent Research Assistant

An intelligent multi-agent system that automates academic research by searching, summarizing, and synthesizing research papers using Large Language Models and Retrieval-Augmented Generation (RAG).

## ✨ Features

- **Multi-Source Search**: Queries 4 academic databases (arXiv, PubMed, Semantic Scholar, OpenAlex) covering 450M+ papers
- **Intelligent Deduplication**: Automatically removes duplicate papers across sources
- **AI-Powered Analysis**: GPT-3.5-powered summarization, synthesis, and fact-checking
- **Semantic Search**: Vector database (ChromaDB) for topic-based paper retrieval
- **Manuscript Review**: Automated evaluation of research manuscripts (structure, citations, readability)
- **Multi-Format Export**: Generate reports in TXT, Markdown, and PDF formats
- **Web Interface**: User-friendly Streamlit UI with real-time progress tracking
- **Cost-Efficient**: ~$0.01 per research query

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │
│   (Port 8501)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   (Port 8000)   │
└────────┬────────┘
         │
         ▼
┌────────────────────────────────────────┐
│         Agent Pipeline                 │
│  ┌──────────────────────────────────┐  │
│  │  1. SearchAgent                  │  │
│  │     - arXiv, PubMed, Semantic    │  │
│  │       Scholar, OpenAlex          │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  2. Vector Store (ChromaDB)      │  │
│  │     - Store & Retrieve Papers    │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  3. SummarizerAgent (GPT-3.5)    │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  4. FactCheckerAgent (GPT-3.5)   │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  5. SynthesisAgent (GPT-3.5)    │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  6. ReviewAgent (GPT-3.5)        │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │  7. ReportGenerator              │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ResearchAI.git
cd ResearchAI
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env  # Linux/Mac

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

### Running the Application

1. Start the FastAPI backend:
```bash
cd src
python api.py
```

2. In a new terminal, start the Streamlit frontend:
```bash
cd src
streamlit run streamlit_app.py
```

3. Open your browser to `http://localhost:8501`

## 📖 Usage

### Research Query

```python
from pipeline import run_research_pipeline

# Run a research query
results = run_research_pipeline(
    query="deep learning optimization techniques",
    max_papers=10
)

# Access results
print(f"Found {len(results['papers'])} papers")
print(f"Executive Summary: {results['synthesis']['executive_summary']}")
print(f"Total Cost: ${results['total_cost']:.4f}")
```

### Manuscript Review

```python
from agents.review_agent import ReviewAgent

reviewer = ReviewAgent()
manuscript_text = "Your research manuscript here..."

review = reviewer.generate_review(manuscript_text)
print(f"Structure Score: {review['structure_score']}%")
print(f"Citation Density: {review['citation_density']}/1000 words")
print(f"Readability: {review['avg_sentence_length']} words/sentence")
```

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Average Query Cost | $0.006 - $0.01 |
| Papers Searched | 450M+ across 4 databases |
| Average Query Time | 30-45 seconds |
| Supported File Formats | TXT, Markdown, PDF |
| Embedding Model | all-MiniLM-L6-v2 (local, free) |
| LLM Model | GPT-3.5-turbo |

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **Academic APIs**: arXiv, PubMed E-utilities, Semantic Scholar, OpenAlex
- **Export**: ReportLab (PDF), Markdown

## 📁 Project Structure

```
ResearchAI/
├── src/
│   ├── agents/
│   │   ├── search_agent.py         # Multi-source paper search
│   │   ├── summarizer_agent.py     # AI summarization
│   │   ├── synthesis_agent.py      # Cross-paper analysis
│   │   ├── fact_checker_agent.py   # Consensus verification
│   │   └── review_agent.py         # Manuscript evaluation
│   ├── api.py                      # FastAPI backend
│   ├── streamlit_app.py            # Web UI
│   ├── pipeline.py                 # Main orchestration
│   ├── vector_store.py             # ChromaDB interface
│   ├── report_generator.py         # Export functionality
│   └── config.py                   # Configuration
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### POST /research
Run a research query
```json
{
  "query": "machine learning in healthcare",
  "max_papers": 10
}
```

### POST /review
Review a manuscript
```json
{
  "manuscript_text": "Your manuscript here...",
  "word_limit": 500
}
```

### GET /health
Check API status


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

Aslican Alacal -aslialacal@hotmail.com

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 API
- arXiv, PubMed, Semantic Scholar, and OpenAlex for academic data access
- Sentence-Transformers for embedding models
- FastAPI and Streamlit teams for excellent frameworks