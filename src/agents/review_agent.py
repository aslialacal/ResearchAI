import os
import re
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ReviewAgent:
    """Automated paper review agent for manuscript evaluation"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.total_cost = 0
        
        self.expected_sections = [
            "abstract", "introduction", "method", "methodology",
            "results", "discussion", "conclusion", "references"
        ]
    
    def analyze_structure(self, text):
        """Check for presence of standard academic sections"""
        text_lower = text.lower()
        found = []
        missing = []
        
        # Create a dict to track which sections are found
        sections_found = {}
        
        for section in self.expected_sections:
            if section in text_lower:
                found.append(section)
                sections_found[section] = True
            else:
                missing.append(section)
                sections_found[section] = False
        
        # Remove duplicates (method/methodology count as one)
        if "method" in found and "methodology" in found:
            found.remove("methodology")
        if "method" in missing and "methodology" in found:
            missing.remove("method")
        
        score = len(found) / (len(self.expected_sections) - 1)
        
        return {
            "sections_found": sections_found,  # Added this
            "found_sections": found,
            "missing_sections": missing,
            "completeness_score": round(score * 100, 1)
    }
    
    def analyze_citations(self, text):
        """Analyze citation patterns"""
        # Match [1], [2,3], (Author, 2020), (Author et al., 2020)
        bracket_citations = len(re.findall(r'\[\d+(?:,\s*\d+)*\]', text))
        author_year = len(re.findall(r'\([A-Z][a-z]+(?:\s+et\s+al\.?)?,?\s*\d{4}\)', text))
        total = bracket_citations + author_year
        
        word_count = len(text.split())
        density = (total / word_count) * 1000 if word_count > 0 else 0
        
        if density < 3:
            assessment = "Low citation density - consider adding more references"
        elif density < 8:
            assessment = "Adequate citation density"
        else:
            assessment = "Good citation density"
        
        return {
            "total_citations": total,
            "density_per_1000_words": round(density, 2),
            "assessment": assessment
        }
    
    def analyze_readability(self, text):
        """Calculate readability metrics"""
        sentences = len(re.findall(r'[.!?]+', text))
        words = len(text.split())
        
        if sentences == 0:
            return {"error": "No sentences detected"}
        
        avg_sentence_length = words / sentences
        
        if avg_sentence_length < 15:
            clarity = "Easy to read - sentences are concise"
        elif avg_sentence_length < 25:
            clarity = "Moderate complexity - appropriate for academic writing"
        else:
            clarity = "Complex sentences - consider breaking up for clarity"
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "clarity_assessment": clarity
        }
    
    def generate_review(self, text, title="Untitled Manuscript"):
        """Generate comprehensive review using LLM"""
        
        print(f"\n Reviewing: {title[:50]}...")
        
        # Run automated analyses
        structure = self.analyze_structure(text)
        citations = self.analyze_citations(text)
        readability = self.analyze_readability(text)
        
        print(f"   Structure completeness: {structure['completeness_score']}%")
        print(f"   Citation density: {citations['density_per_1000_words']} per 1000 words")
        print(f"   Avg sentence length: {readability.get('avg_sentence_length', 'N/A')} words")
        
        # Truncate for LLM
        text_for_llm = text[:10000] if len(text) > 10000 else text
        
        prompt = f"""You are an academic peer reviewer. Analyze this manuscript and provide a structured review.

MANUSCRIPT TITLE: {title}

MANUSCRIPT TEXT:
{text_for_llm}

AUTOMATED ANALYSIS:
- Structure completeness: {structure['completeness_score']}%
- Missing sections: {', '.join(structure['missing_sections']) if structure['missing_sections'] else 'None'}
- Citation density: {citations['density_per_1000_words']} per 1000 words
- Average sentence length: {readability.get('avg_sentence_length', 'N/A')} words

Provide your review in this exact format:

## SUMMARY
(2-3 sentences summarizing the paper's main contribution)

## STRENGTHS
- (list 3-4 key strengths)

## WEAKNESSES
- (list 3-4 areas needing improvement)

## DETAILED FEEDBACK
(Specific suggestions for improving the manuscript)

## RECOMMENDATION
(Choose one: Accept, Minor Revisions, Major Revisions, or Reject)

## JUSTIFICATION
(2-3 sentences explaining your recommendation)
"""
        
        print("   Generating AI review...")
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        
        llm_review = response.choices[0].message.content
        
        # Calculate cost
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = (input_tokens * 0.0015 / 1000) + (output_tokens * 0.002 / 1000)
        self.total_cost = cost
        
        print(f"   Review complete! Cost: ${cost:.4f}")
        
        return {
            "title": title,
            "automated_analysis": {
                "structure": structure,
                "citations": citations,
                "readability": readability
            },
            "llm_review": llm_review,
            "total_cost": cost,
            "generated_at": datetime.now().isoformat(),
            "disclaimer": "This is an automated pre-review. It does not replace human peer review."
        }
    
    def format_review_report(self, review):
        """Format review into readable report"""
        report = "=" * 60 + "\n"
        report += "AUTOMATED MANUSCRIPT REVIEW\n"
        report += "=" * 60 + "\n\n"
        
        report += f"Title: {review['title']}\n"
        report += f"Date: {review['generated_at'][:10]}\n\n"
        
        report += "-" * 40 + "\n"
        report += "AUTOMATED METRICS\n"
        report += "-" * 40 + "\n"
        
        analysis = review['automated_analysis']
        report += f"Structure Completeness: {analysis['structure']['completeness_score']}%\n"
        report += f"Found Sections: {', '.join(analysis['structure']['found_sections'])}\n"
        if analysis['structure']['missing_sections']:
            report += f"Missing Sections: {', '.join(analysis['structure']['missing_sections'])}\n"
        report += f"\nCitation Density: {analysis['citations']['density_per_1000_words']} per 1000 words\n"
        report += f"Citation Assessment: {analysis['citations']['assessment']}\n"
        report += f"\nWord Count: {analysis['readability']['word_count']}\n"
        report += f"Avg Sentence Length: {analysis['readability'].get('avg_sentence_length', 'N/A')} words\n"
        report += f"Clarity: {analysis['readability'].get('clarity_assessment', 'N/A')}\n\n"
        
        report += "-" * 40 + "\n"
        report += "AI REVIEWER FEEDBACK\n"
        report += "-" * 40 + "\n"
        report += review['llm_review'] + "\n\n"
        
        report += "-" * 40 + "\n"
        report += f"Review Cost: ${review['total_cost']:.4f}\n"
        report += f"\n⚠️ {review['disclaimer']}\n"
        
        return report