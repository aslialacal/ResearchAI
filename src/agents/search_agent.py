"""
Search Agent: Searches arXiv for relevant papers on a given topic
"""
import arxiv
import json
from datetime import datetime
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import MAX_PAPERS_TO_FETCH, CACHE_DIR

class SearchAgent:
    """Agent responsible for searching academic papers"""
    
    def __init__(self, max_results=MAX_PAPERS_TO_FETCH):
        self.max_results = max_results
        self.papers = []
    
    def search_arxiv(self, query, max_results=None):
        """
        Search arXiv for papers matching the query
        Args:
            query (str): Search query
            max_results (int): Maximum number of papers to return
        Returns:
            list: List of paper metadata dictionaries
        """
        
        if max_results is None:
            max_results = self.max_results
        
        print(f"\n Searching arXiv for: '{query}'")
        print(f"   Fetching up to {max_results} papers...\n")
        
        try:
            # Create arXiv search client
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            # Execute search and process results
            self.papers = []
            for result in client.results(search):
                paper = {
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'published': result.published.strftime('%Y-%m-%d'),
                    'summary': result.summary,
                    'arxiv_id': result.entry_id.split('/')[-1],
                    'pdf_url': result.pdf_url,
                    'categories': result.categories,
                    "source": "arXiv"
                }
                self.papers.append(paper)
                
                # Print preview
                print(f" Found: {paper['title'][:80]}...")
                print(f" Authors: {', '.join(paper['authors'][:3])}")
                print(f" Published: {paper['published']}\n")
            
            print(f" Total papers found: {len(self.papers)}\n")
            return self.papers
            
        except Exception as e:
            print(f" Error searching arXiv: {str(e)}")
            return []
    
    def search_pubmed(self, query, max_results=None):
        """Search arXiv for papers matching the query"""
        import requests
        import xml.etree.ElementTree as ET
        
        if max_results is None:
            max_results = self.max_results
        
        print(f"\n Searching PubMed for: '{query}'")
        print(f"  Fetching up to {max_results} papers...")
        
        #Search for paper IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db" : "pubmed",
            "term": query,
            "retmax": max_results,
            "sort" : "relevance"
        }
        
        try:
            response = requests.get(search_url, params=search_params)
            root = ET.fromstring(response.content)
            id_list = [id_elem.text for id_elem in root.findall(".//Id")]
            
            if not id_list:
                print("No papers found on PubMed")
                return []
            
            #Fetch Paper details
            fetch_url= "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "rettype": "abstract",
                "retmode": "xml"
            }
            
            response= requests.get(fetch_url, params= fetch_params)
            root = ET.fromstring(response.content)
            
            self.pubmed_papers = []
            for article in root.findall(".//PubmedArticle"):
                try:
                    title = article.find(".//ArticleTitle").text or "No title"
                    
                    abstract_elem = article.find(".//AbstractText")
                    summary = abstract_elem.text if abstract_elem is not None else "No abstract available"
                    
                    authors = []
                    for author in article.findall(".//Author"):
                        lastname = author.find("LastName")
                        forename = author.find("ForeName")
                        if lastname is not None and forename is not None:
                            authors.append(f"{forename.text} {lastname.text}")
                            
                    pmid = article.find(".//PMID").text
                    
                    pub_date = article.find(".//PubDate/Year")
                    year = pub_date.text if pub_date is not None else "Unknown"
                    
                    paper={
                        "title" : title,
                        "authors": authors if authors else ["Unknown"],
                        "published": year,
                        "summary": summary,
                        "arxiv_id": f"PMID:{pmid}",
                        "pdf_url" : f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                        "source": "pubmed"
                    }
                    
                    self.pubmed_papers.append(paper)
                    print(f"\n Found: {title[:70]}....")
                
                except Exception as e:
                    continue
        
            print(f"\n Total papers found: {len(self.pubmed_papers)}")
            return self.pubmed_papers
        
        except Exception as e:
            print(f" PubMed search error: {e}")
            return []

    
    def search_semantic_scholar(self, query, max_results=None):
        """Search Semantic Scholar for papers"""
        import requests
        
        if max_results is None:
            max_results = self.max_results
        
        print(f"\n Searching Semantic Scholar for: '{query}'")
        print(f"  Fetching up to {max_results} papers...")
        
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,abstract,paperId,url"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if "data" not in data or not data["data"]:
                print("No papers found on Semantic Scholar")
                return []
            
            self.semantic_papers = []
            for item in data["data"]:
                authors = [a["name"] for a in item.get("authors", [])] if item.get("authors") else ["Unknown"]
                
                paper = {
                    "title": item.get("title", "No title"),
                    "authors": authors,
                    "published": str(item.get("year", "Unknown")),
                    "summary": item.get("abstract") or "No abstract available",
                    "arxiv_id": f"S2:{item.get('paperId', 'unknown')}",
                    "pdf_url": item.get("url", ""),
                    "source": "semantic_scholar"
                }
                
                self.semantic_papers.append(paper)
                print(f"\n Found: {paper['title'][:70]}...")
            
            print(f"\n Total papers found: {len(self.semantic_papers)}")
            return self.semantic_papers
        
        except Exception as e:
            print(f" Semantic Scholar search error: {e}")
            return []
    
    def search_openalex(self, query, max_results=None):
        """Search OpenAlex for papers with citation data"""
        import requests
        
        if max_results is None:
            max_results = self.max_results
        
        print(f"\n Searching OpenAlex for: '{query}'")
        print(f"  Fetching up to {max_results} papers...")
        
        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per_page": max_results,
            "sort": "relevance_score:desc"
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if "results" not in data or not data["results"]:
                print("No papers found on OpenAlex")
                return []
            
            self.openalex_papers = []
            for item in data["results"]:
                authors = [a["author"]["display_name"] for a in item.get("authorships", [])] if item.get("authorships") else ["Unknown"]
                
                paper = {
                    "title": item.get("title", "No title"),
                    "authors": authors,
                    "published": str(item.get("publication_year", "Unknown")),
                    "summary": item.get("abstract") or "No abstract available",
                    "arxiv_id": f"OA:{item.get('id', 'unknown').split('/')[-1]}",
                    "pdf_url": item.get("primary_location", {}).get("pdf_url") or item.get("doi", ""),
                    "citations": item.get("cited_by_count", 0),
                    "source": "openalex"
                }
                
                self.openalex_papers.append(paper)
                print(f"\n Found: {paper['title'][:70]}...")
                print(f"   Citations: {paper['citations']}")
            
            print(f"\n Total papers found: {len(self.openalex_papers)}")
            return self.openalex_papers
        
        except Exception as e:
            print(f" OpenAlex search error: {e}")
            return []
        
    def deduplicate_papers(self, papers):
        """Remove duplicate papers based on title similarity"""
        import re
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            # Normalize: lowercase, remove punctuation, extra spaces
            normalized = paper['title'].lower().strip()
            normalized = re.sub(r'[^\w\s]', '', normalized)  # remove punctuation
            normalized = re.sub(r'\s+', ' ', normalized)     # single spaces
            
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique_papers.append(paper)
        
        removed = len(papers) - len(unique_papers)
        if removed > 0:
            print(f"\n Removed {removed} duplicate papers")
        
        return unique_papers
    
    def save_results(self, filename=None):
        """Save search results to JSON file"""
        if not self.papers:
            print(" No papers to save!")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"search_results_{timestamp}.json"
                
        filepath = CACHE_DIR / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.papers, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(self.papers)} papers to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f" Error saving results: {str(e)}")
            return None
    
    def get_paper_summaries(self):
        """Get quick overview of all papers"""
        summaries = []
        for i, paper in enumerate(self.papers, 1):
            summaries.append({
                'number': i,
                'title': paper['title'],
                'year': paper['published'][:4],
                'summary_preview': paper['summary'][:150] + "..."
            })
        return summaries