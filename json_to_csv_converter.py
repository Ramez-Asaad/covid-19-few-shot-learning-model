import json
import pandas as pd
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_paper(paper: dict) -> dict:
    """Process a single paper entry to prepare it for CSV conversion."""
    try:
        # Extract author names and join with semicolons
        author_names = [author['name'] for author in paper['authors']]
        author_affiliations = [author['affiliation'] for author in paper['authors']]
        author_emails = [author['email'] for author in paper['authors']]
        
        processed_paper = {
            'title': paper['title'],
            'abstract': paper['abstract'],
            'category': paper['category'],
            'date_published': paper['date_published'],
            'authors': '; '.join(author_names),
            'author_affiliations': '; '.join(author_affiliations),
            'author_emails': '; '.join(author_emails),
            'keywords': '; '.join(paper['keywords']),
            'journal': paper['journal'],
            'citation_count': paper['citation_count'],
            'reference_count': paper['reference_count']
        }
        return processed_paper
    except Exception as e:
        logger.warning(f"Error processing paper: {str(e)}")
        return None

def convert_json_to_csv(
    json_file_path: str = "synthetic_covid19_papers.json",
    output_csv_path: str = "synthetic_covid19_papers.csv"
) -> None:
    """
    Convert the synthetic COVID-19 papers from JSON to CSV format.
    
    Args:
        json_file_path (str): Path to the input JSON file
        output_csv_path (str): Path to save the output CSV file
    """
    try:
        logger.info(f"Starting conversion of {json_file_path} to CSV...")
        
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        logger.info(f"Found {len(papers)} records to process")
        
        # Process each paper
        processed_papers = []
        for paper in tqdm(papers, desc="Processing papers"):
            processed_paper = process_paper(paper)
            if processed_paper:
                processed_papers.append(processed_paper)
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_papers)
        
        # Save to CSV
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        logger.info(f"Successfully converted to CSV. Output saved to: {output_csv_path}")
        
        # Display sample and statistics
        logger.info("\nFirst few rows of the converted data:")
        logger.info(df.head())
        
        logger.info("\nDataset statistics:")
        logger.info(f"Number of records: {len(df)}")
        logger.info(f"Number of columns: {len(df.columns)}")
        logger.info("Columns:")
        for col in df.columns:
            logger.info(f"  - {col}")
        
        logger.info("\nCategory distribution:")
        category_dist = df['category'].value_counts()
        for category, count in category_dist.items():
            logger.info(f"  {category}: {count} papers")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(f"Error details: {str(e)}")
        raise

if __name__ == "__main__":
    convert_json_to_csv() 