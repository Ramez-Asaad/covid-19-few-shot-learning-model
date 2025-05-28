import requests
import json
import logging
import time
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_sample_data(output_file: str = "cord19_sample.json", sample_size: int = 20):
    """
    Download and create a sample dataset from the Semantic Scholar COVID-19 Open Research Dataset.
    This uses the Semantic Scholar API to get a small sample of COVID-19 related papers.
    
    Args:
        output_file (str): Path to save the sampled dataset
        sample_size (int): Number of papers to include in the sample
    """
    try:
        # Semantic Scholar API endpoint for COVID-19 papers
        api_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        
        # Parameters for the API request
        params = {
            "query": "COVID-19 treatment",
            "limit": min(sample_size, 20),  # Limit to 20 papers per request
            "fields": "title,abstract,year,authors,venue,citations,references"
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"Downloading {sample_size} papers from Semantic Scholar API")
        response = requests.get(api_url, params=params, headers=headers)
        
        # Handle rate limiting
        if response.status_code == 429:
            logger.info("Rate limited. Waiting 5 seconds before retrying...")
            time.sleep(5)
            response = requests.get(api_url, params=params, headers=headers)
        
        response.raise_for_status()
        papers = response.json().get('data', [])
        
        # Transform the data to match our needs
        processed_papers = []
        for paper in papers:
            # Extract keywords from the title and abstract
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
            
            # Simple keyword extraction (you can make this more sophisticated)
            keywords = ['treatment', 'vaccine', 'diagnosis', 'epidemiology']
            category = next((k for k in keywords if k.lower() in text.lower()), 'general')
            
            processed_paper = {
                'title': paper.get('title', ''),
                'abstract': paper.get('abstract', ''),
                'year': paper.get('year'),
                'authors': [author.get('name', '') for author in paper.get('authors', [])],
                'venue': paper.get('venue', ''),
                'citation_count': len(paper.get('citations', [])),
                'reference_count': len(paper.get('references', [])),
                'category': f'covid-19-{category}'
            }
            processed_papers.append(processed_paper)
        
        # Save the processed papers
        logger.info(f"Saving {len(processed_papers)} papers to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_papers, f, indent=2, ensure_ascii=False)
            
        logger.info("Sample dataset created successfully")
        logger.info("\nCategory distribution:")
        categories = {}
        for paper in processed_papers:
            cat = paper['category']
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in categories.items():
            logger.info(f"  {cat}: {count} papers")
        
    except Exception as e:
        logger.error(f"Error downloading sample data: {str(e)}")
        raise

if __name__ == "__main__":
    download_sample_data() 