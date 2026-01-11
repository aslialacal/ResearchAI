"""
Configuration settings for ResearchAI
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
CACHE_DIR = DATA_DIR / "cache"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# LLM Settings
DEFAULT_MODEL = "gpt-3.5-turbo"  
MAX_TOKENS = 2000
TEMPERATURE = 0.3  

# Search Settings
MAX_PAPERS_TO_FETCH = 10  
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"

def validate_config():
    
    issues = []
    
    if not OPENAI_API_KEY:
        issues.append("OPENAI_API_KEY not found in .env file")
    
    if issues:
        print("\nConfiguration Issues:")
        for issue in issues:
            print(f"   {issue}")
        return False
    
    print(" Configuration valid!")
    return True

if __name__ == "__main__":
    # Test configuration
    validate_config()
