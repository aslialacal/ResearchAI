
import openai
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DEFAULT_MODEL, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class FactCheckerAgent:
    """Verifies claims by cross-referencing papers"""
    
    def __init__(self):
        self.model = DEFAULT_MODEL
        self.total_cost = 0.0
        
    def fact_check(self, papers, query):
        """
        Cross-reference claims across papers
        Returns fact-check report with consensus/contradictions
        """
        
        if len(papers) < 2:
            return "Insufficient papers for fact-checking (need at least 2)"
        
        # Extract all summaries
        summaries = []
        for i, paper in enumerate(papers, 1):
            if 'ai_summary' in paper:
                summaries.append(f"Paper {i} [{paper.get('source', 'unknown').upper()}]: {paper['title']}\n{paper['ai_summary']}")
        
        if not summaries:
            return "No summaries available for fact-checking"
        
        combined_summaries = "\n\n---\n\n".join(summaries)
        
        # Fact-checking prompt
        prompt = f"""You are a rigorous fact-checker analyzing research papers on: {query}

Review these paper summaries and identify:

1. CONSENSUS FINDINGS: Claims supported by multiple papers
2. CONTRADICTIONS: Where papers disagree or contradict each other
3. ISOLATED CLAIMS: Important findings mentioned by only one paper (flag as "needs verification")
4. CONFIDENCE ASSESSMENT: Rate overall reliability (High/Medium/Low) based on agreement

Be specific - cite which papers support or contradict each finding.

SUMMARIES:
{combined_summaries}

Provide your fact-check analysis:"""
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a scientific fact-checker specializing in cross-referencing research claims."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1200
            )
            
            fact_check_report = response.choices[0].message.content
            
            # Calculate cost
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            cost = (prompt_tokens * 0.0015 + completion_tokens * 0.002) / 1000
            self.total_cost += cost
            
            print(f"✓ Fact-checking complete (Cost: ${cost:.4f})")
            
            return fact_check_report
            
        except Exception as e:
            print(f"✗ Fact-checking failed: {str(e)}")
            return f"Fact-checking error: {str(e)}"