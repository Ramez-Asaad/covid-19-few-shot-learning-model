import json
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_json_to_notebook(input_file: str, output_file: str = None):
    """
    Convert a JSON file containing notebook data to a proper .ipynb file.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str, optional): Path for the output .ipynb file. 
                                   If None, will use input filename with .ipynb extension
    """
    try:
        # Read the JSON file
        logger.info(f"Reading input file: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        
        # If no output file specified, use input filename with .ipynb extension
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.ipynb'))
        
        # Write the notebook file
        logger.info(f"Writing notebook to: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=1)
        
        logger.info("Conversion completed successfully!")
        return True
        
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    # Get input file from command line argument or use default
    input_file = "CORD_19_few_shot_learning.ipynb"
    output_file = None  # Will use same name with .ipynb extension
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    success = convert_json_to_notebook(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 