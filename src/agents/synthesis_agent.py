import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

#combines multiple paper summaries into coherent analysis
class SynthesisAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.total_cost = 0
        
    #generates synthesis from multiple papers
    def synthesize(self, papers, query):
        if not papers:
            return "No papers to synthesize"
        
        #prepare papers sumaries for synthesis
        paper_texts = []
        for i, paper in enumerate(papers, 1):
            summary = paper.get('ai_summary', paper.get('summary', 'no summary'))
            paper_texts.append(f"Paper {i}: {paper['title']}\n {summary}")
            
        combined_text = "\n\n".join(paper_texts)
        
        # Truncate if too long
        if len(combined_text) > 12000:
            combined_text = combined_text[:12000] + "..."
        
        prompt = f"""You are an expert research analyst. Based on the following {len(papers)} academic papers about "{query}", provide a comprehensive synthesis.

PAPERS:
{combined_text}

Provide your synthesis in this exact format:

## EXECUTIVE SUMMARY
(2-3 sentences summarizing the overall state of research on this topic)

## KEY THEMES
(Identify 3-5 major themes or findings that appear across multiple papers)

## AREAS OF CONSENSUS
(What do most researchers agree on?)

## AREAS OF DEBATE
(Where do researchers disagree or have conflicting findings?)

## RESEARCH GAPS
(What questions remain unanswered? What future research is needed?)

## CONCLUSION
(2-3 sentences with your overall assessment of the research landscape)
"""
        
        print("\n Generating synthesis from all papers...")
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500
        )
        synthesis = response.choices[0].message.content
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = (input_tokens * 0.0015 / 1000) + (output_tokens * 0.002 / 1000)
        self.total_cost = cost
        
        print(f" Synthesis complete! Cost: ${cost:.4f}")
        
        return synthesis
    