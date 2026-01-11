





from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from pipeline import run_research_pipeline
from config import OUTPUT_DIR
from agents.review_agent import ReviewAgent
from datetime import datetime

app = FastAPI(
    title="ResearchAI API",
    description="Multi-source academic research automation",
    version="1.0"
)

# Allow Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchQuery(BaseModel):
    query: str
    max_papers: int = 10

class ResearchResponse(BaseModel):
    status: str
    query: str
    report_file: str
    message: str

@app.post("/review")
def review_endpoint(title: str = "Untitled Manuscript", text: str = ""):
    """Review a manuscript"""
    
    if not text or len(text.strip()) < 100:
        raise HTTPException(status_code=400, detail="Manuscript text must be at least 100 characters")
    
    try:
        reviewer = ReviewAgent()
        
        # generate_review() already returns a complete review dict
        review = reviewer.generate_review(text, title)
        
        # format_review_report() expects the complete review dict
        formatted_report = reviewer.format_review_report(review)
        
        return {
            "status": "success",
            "review": review,
            "formatted_report": formatted_report
        }
    
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}\n{traceback.format_exc()}")


@app.post("/research")
def research_endpoint(query_data: ResearchQuery):
    """Trigger research pipeline"""
    
    try:
        # Run pipeline (this saves reports automatically)
        run_research_pipeline(query_data.query, max_papers=query_data.max_papers)
        
        # Find the most recent report file
        report_files = sorted(OUTPUT_DIR.glob("research_report_*.txt"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not report_files:
            raise HTTPException(status_code=500, detail="Report generation failed")
        
        latest_report = report_files[0]
        
        return {
            "status": "success",
            "query": query_data.query,
            "report_file": str(latest_report),
            "message": f"Research completed! Found relevant papers.",
            "papers_found": query_data.max_papers,
            "cost": 0.01  # Approximate
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@app.get("/results/{filename}")
def get_results(filename: str):
    """Retrieve a specific report"""
    
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return {
        "filename": filename,
        "content": content
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "ResearchAI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)