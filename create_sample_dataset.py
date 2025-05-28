import json
import pandas as pd
import random
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_dataset(input_file: str, output_file: str, sample_size: int = 100):
    """
    Create a smaller sample dataset from the CORD-19 metadata.
    
    Args:
        input_file (str): Path to the input JSON metadata file
        output_file (str): Path to save the sampled dataset
        sample_size (int): Number of papers to include in the sample
    """
    try:
        # Read the JSON file
        logger.info(f"Reading input file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Ensure we don't try to sample more than available
        total_papers = len(data)
        sample_size = min(sample_size, total_papers)
        
        # Randomly sample papers
        logger.info(f"Sampling {sample_size} papers from {total_papers} total papers")
        sampled_data = random.sample(data, sample_size)
        
        # Create categories for few-shot learning
        # We'll categorize papers based on their keywords/topics
        for paper in sampled_data:
            keywords = paper.get('keywords', [])
            if keywords:
                # Use the first keyword as a simple category
                paper['category'] = keywords[0]
            else:
                paper['category'] = 'uncategorized'
        
        # Save the sampled dataset
        logger.info(f"Saving sampled dataset to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sampled_data, f, indent=2, ensure_ascii=False)
        
        # Create a summary of the categories
        categories = {}
        for paper in sampled_data:
            cat = paper['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        logger.info("Category distribution in sample:")
        for cat, count in categories.items():
            logger.info(f"  {cat}: {count} papers")
            
    except Exception as e:
        logger.error(f"Error creating sample dataset: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = "CORD-19-research-challenge-metadata.json"
    output_file = "cord19_sample.json"
    create_sample_dataset(input_file, output_file) 