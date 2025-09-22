# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LitReview is a Python-based tool for extracting species names from academic literature using TaxoNERD (Named Entity Recognition for taxonomic entities). It's designed for PhD students and researchers to automatically identify organisms mentioned in research papers from CSV files.

## Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Main Script
```bash
# Basic usage (analyzes 'abstract' column by default)
python scripts/extract_species.py data/input/your_papers.csv

# Specify different text column
python scripts/extract_species.py data/input/your_papers.csv --text-column title

# Custom output location
python scripts/extract_species.py data/input/your_papers.csv --output data/output/custom_results.csv

# Test with example data
python scripts/extract_species.py data/input/example_papers.csv
```

### Development
```bash
# Check dependencies
pip list | grep -E "(taxonerd|pandas|spacy)"

# Verify CSV structure
python -c "import pandas as pd; print(pd.read_csv('data/input/file.csv').columns.tolist())"
```

## Architecture

### Project Structure
```
LitReview/
├── data/
│   ├── input/          # CSV files to process
│   └── output/         # Generated results
├── scripts/
│   └── extract_species.py  # Main processing script
├── requirements.txt    # Python dependencies
└── README.md          # User documentation
```

### Core Components

1. **TaxoNERD Integration** (`scripts/extract_species.py:setup_taxonerd()`):
   - Loads pre-trained biomedical NER model
   - Handles model initialization and error cases

2. **CSV Processing Pipeline** (`scripts/extract_species.py:process_csv()`):
   - Reads input CSV files with pandas
   - Validates column existence
   - Processes each row through TaxoNERD
   - Generates output with extracted species and summary statistics

3. **Entity Extraction** (`scripts/extract_species.py:extract_species_from_text()`):
   - Uses TaxoNERD to identify "TAXON" entities
   - Deduplicates species names per text
   - Handles edge cases (empty text, NaN values)

### Data Flow
1. User provides CSV with text column (abstracts, titles, etc.)
2. Script validates input and loads TaxoNERD model
3. Each row's text is processed to extract taxonomic entities
4. Results saved as enhanced CSV + species summary file
5. Console output provides processing statistics

## Key Dependencies

- **taxonerd**: Core NER functionality for taxonomic entities
- **pandas**: CSV processing and data manipulation
- **spacy**: Underlying NLP framework (used by taxonerd)

## Development Notes

- Script designed for beginner-friendly modification
- Command-line interface with helpful error messages
- Processing can be slow (5-10 minutes for 100 papers) due to NER complexity
- Model downloads automatically on first run (~1GB)
- Virtual environment strongly recommended due to large ML dependencies