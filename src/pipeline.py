
#Imports

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent
from datetime import datetime
from vector_store import VectorStore
from agents.synthesis_agent import SynthesisAgent
from report_generator import generate_markdown_report, generate_pdf_report
from agents.fact_checker_agent import FactCheckerAgent



#Main function
def run_research_pipeline(query, max_papers=5):
    """
    Search → Store in Vector DB → Semantic Search → Summarize → Report
    """
    
    print(f"\n Research Query: {query}")
    print(f" Processing up to {max_papers} papers")
    print("STEP 1: SEARCHING FOR PAPERS")
    print("-" * 70)
    
    search_agent = SearchAgent(max_results=max_papers)
    
    arxiv_papers = search_agent.search_arxiv(query)
    pubmed_papers = search_agent.search_pubmed(query)
    semantic_papers = search_agent.search_semantic_scholar(query)
    openalex_papers = search_agent.search_openalex(query)

    # Combine results
    all_papers = arxiv_papers + pubmed_papers + semantic_papers + openalex_papers

    # Remove duplicates
    papers = search_agent.deduplicate_papers(all_papers)
    print(f" Unique papers after deduplication: {len(papers)}")

    
    if not papers:
        print(" No papers found ")
        return
    
    search_agent.save_results()
    
    # STEP 2: Store in vector database
    
    print("\nSTEP 2: STORING IN VECTOR DATABASE")
    print("-"*70)
    vector_store = VectorStore()
    vector_store.add_papers(papers)
    print(f"Stored {len(papers)} papers with embeddings")
    
    
    #STEP 3: Semantic Search for most relevant papers
    
    print("\nSTEP 3:FINDING MOST REVELANT PAPERS")
    print("-"*70)
    results = vector_store.search_similar(query, n_results=10)
    relevant_paper_ids = results['ids'][0]
    
    #Get full paper data for relevant paper
    
    relevant_papers = [p for p in papers if p['arxiv_id'] in relevant_paper_ids]
    print(f" Found {len(relevant_papers)} most relevant papers")
    
        
    #STEP 4: Summary relevnt papers
    
    print("\nSTEP 4: SUMMARIZING PAPERS WITH AI")
    print("-"*70)
    summarizer = SummarizerAgent()
    enhanced_papers =summarizer.summarize_multiple(relevant_papers)
    

    
    # STEP 5: Synthesize findings
    print("\nSTEP 5: SYNTHESIZING FINDINGS")
    print("-"*70)
    synthesis_agent = SynthesisAgent()
    synthesis = synthesis_agent.synthesize(enhanced_papers, query)
    
    # STEP 6: Fact-check findings
    print("\nSTEP 6 : FACT-CHECKING FINDINGS")
    print("-"*70)
    fact_checker = FactCheckerAgent()
    fact_check_report = fact_checker.fact_check(enhanced_papers, query)
        
    # STEP 7: Generate report
    print("\nSTEP 7: GENERATING REPORT")
    print("-"*70)
    total_cost = summarizer.total_cost + synthesis_agent.total_cost + fact_checker.total_cost
    report = generate_report(query, enhanced_papers, total_cost, synthesis)
    
    
    # Save reports in multiple formats
    
    from config import OUTPUT_DIR
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save TXT
    report = generate_report(query, enhanced_papers, total_cost, synthesis, fact_check_report)
    txt_file = OUTPUT_DIR / f"research_report_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n TXT Report saved to: {txt_file}")
    
    # Save Markdown
    md_report = generate_markdown_report(query, enhanced_papers, total_cost, synthesis, fact_check_report)
    md_file = OUTPUT_DIR / f"research_report_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f" Markdown Report saved to: {md_file}")
    
    # Save PDF
    pdf_file = OUTPUT_DIR / f"research_report_{timestamp}.pdf"
    generate_pdf_report(query, enhanced_papers, total_cost, synthesis, fact_check_report, pdf_file)
    print(f" PDF Report saved to: {pdf_file}")
    
# Creates the text report

def generate_report(query, papers, total_cost, synthesis="", fact_check=""):
    """Generate a text report"""
    report = f"RESEARCH REPORT\n"
    report += f"Query: {query}\n"
    report += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    if synthesis:
        report += "=" * 60 + "\n"
        report += "SYNTHESIS OF FINDINGS\n"
        report += "=" * 60 + "\n"
        report += synthesis + "\n\n"
        
    if fact_check:
        report += "=" * 60 + "\n"
        report += "FACT-CHECKING ANALYSIS\n"
        report += "=" * 60 + "\n"
        report += fact_check + "\n\n"
    
    report += "=" * 60 + "\n"
    report += "INDIVIDUAL PAPER SUMMARIES\n"
    report += "=" * 60 + "\n\n"
    
    for i, paper in enumerate(papers, 1):
        report += f"{i}. [{paper.get('source', 'unknown').upper()}] {paper['title']}\n"
        report += f"   Authors: {paper['authors']}\n"
        if 'ai_summary' in paper:
            report += f"   Summary: {paper['ai_summary']}\n"
        if 'citations' in paper:
            report += f"   Citations: {paper['citations']}\n"
        report += "\n"
    
    report += f"\nTotal API Cost: ${total_cost:.4f}\n"
    
    return report

if __name__ == "__main__":
    run_research_pipeline("low current security systems and machine learning", max_papers=10) 