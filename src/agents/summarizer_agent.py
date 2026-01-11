""" Summarizer Agent
Uses LLM to summarize research papers
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_TOKENS, validate_config
import json

class SummarizerAgent:
    """Agent responsible for summarizing research papers using LLM"""
    
    def __init__(self):
        if not validate_config():
            raise ValueError("Configuration validation failed")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.total_cost = 0.0
    
    def summarize_paper(self, paper_data):
        """
        Summarize a single research paper
        
        Args:
            paper_data (dict): Paper metadata including title, authors, summary
            
        Returns:
            dict: Enhanced paper data with AI-generated summary
        """
        title = paper_data.get('title', 'Unknown')
        abstract = paper_data.get('summary', '')
        
        print(f"\n Summarizing: {title[:60]}...")
        
        # Create prompt for summarization
        prompt = f"""You are a research assistant. Summarize this academic paper in a clear, structured format.

Paper Title: {title}
Abstract: {abstract}

Provide a summary with these sections:
1. Main Research Question (1 sentence)
2. Key Methodology (2-3 sentences)
3. Main Findings (2-3 sentences)
4. Significance (1-2 sentences)

Keep it concise and technical but understandable."""

        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert research analyst who creates clear, concise paper summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content
            
            # Calculate cost
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = (input_tokens / 1000 * 0.0015) + (output_tokens / 1000 * 0.002)
            self.total_cost += cost
            
            # Add summary to paper data
            enhanced_paper = paper_data.copy()
            enhanced_paper['ai_summary'] = summary
            enhanced_paper['tokens_used'] = {
                'input': input_tokens,
                'output': output_tokens,
                'cost': cost
            }
            
            print(f"   ✅ Done! Cost: ${cost:.6f}")
            
            return enhanced_paper
            
        except Exception as e:
            print(f" Error: {str(e)}")
            return paper_data
    
    def summarize_multiple(self, papers):
        """
        Summarize multiple papers
        
        Args:
            papers (list): List of paper dictionaries
            
        Returns:
            list: Enhanced papers with summaries
        """
        print(f"\n Starting batch summarization of {len(papers)} papers...")
        
        enhanced_papers = []
        for i, paper in enumerate(papers, 1):
            print(f"\nProgress: {i}/{len(papers)}")
            enhanced = self.summarize_paper(paper)
            enhanced_papers.append(enhanced)
        
        print(f"\n Total cost for {len(papers)} papers: ${self.total_cost:.6f}")
        
        return enhanced_papers
    
    def save_summaries(self, papers, filename):
        """Save summarized papers to JSON"""
        from config import OUTPUT_DIR
        
        filepath = OUTPUT_DIR / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(papers, f, indent=2, ensure_ascii=False)
            
            print(f"\n Saved summaries to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f" Error saving: {str(e)}")
            return None
