#!/usr/bin/env python3
"""
Literature Review Species Extractor

This script uses TaxoNERD to extract species names from research papers listed in a CSV file.
Perfect for organizing literature reviews by the organisms studied.

Author: Created for PhD research
"""

import pandas as pd
import taxonerd
from pathlib import Path
import argparse
import sys
from collections import Counter

def setup_taxonerd():
    """
    Initialize TaxoNERD model.
    This downloads the model if it's not already installed.
    """
    print("Loading TaxoNERD model...")
    try:
        # Load the pre-trained model
        nlp = taxonerd.TaxoNERD(model="en_core_eco_biobert", prefer_gpu=False)
        print("✓ TaxoNERD model loaded successfully!")
        return nlp
    except Exception as e:
        print(f"❌ Error loading TaxoNERD: {e}")
        print("Make sure you've installed the requirements: pip install -r requirements.txt")
        sys.exit(1)

def extract_species_from_text(nlp, text):
    """
    Extract taxonomic entities from a given text.

    Args:
        nlp: TaxoNERD model
        text: Text to analyze

    Returns:
        list: List of unique species/taxonomic entities found
    """
    if pd.isna(text) or not text.strip():
        return []

    # Process the text with TaxoNERD
    doc = nlp(str(text))

    # Extract unique taxonomic entities
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["TAXON"]:  # TaxoNERD labels taxonomic entities as "TAXON"
            entities.append(ent.text.strip())

    # Return unique entities
    return list(set(entities))

def process_csv(input_file, text_column, output_file=None):
    """
    Process a CSV file and extract species from the specified text column.

    Args:
        input_file: Path to input CSV file
        text_column: Name of the column containing text to analyze
        output_file: Path for output file (optional)
    """
    # Load the CSV file
    print(f"📖 Reading CSV file: {input_file}")
    try:
        df = pd.read_csv(input_file)
        print(f"✓ Loaded {len(df)} rows")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    # Check if the specified column exists
    if text_column not in df.columns:
        print(f"❌ Column '{text_column}' not found in CSV.")
        print(f"Available columns: {', '.join(df.columns)}")
        return

    # Initialize TaxoNERD
    nlp = setup_taxonerd()

    # Extract species from each row
    print(f"🔍 Extracting species from '{text_column}' column...")
    all_species = []
    df['extracted_species'] = None
    df['species_count'] = 0

    for idx, row in df.iterrows():
        text = row[text_column]
        species = extract_species_from_text(nlp, text)

        # Store results
        df.at[idx, 'extracted_species'] = '; '.join(species) if species else ''
        df.at[idx, 'species_count'] = len(species)
        all_species.extend(species)

        # Progress indicator
        if (idx + 1) % 10 == 0:
            print(f"  Processed {idx + 1}/{len(df)} rows...")

    print(f"✓ Processing complete!")

    # Generate summary statistics
    species_counter = Counter(all_species)
    total_unique_species = len(species_counter)
    papers_with_species = len(df[df['species_count'] > 0])

    print(f"\n📊 SUMMARY:")
    print(f"  • Total papers processed: {len(df)}")
    print(f"  • Papers with species mentions: {papers_with_species}")
    print(f"  • Total unique species found: {total_unique_species}")

    if total_unique_species > 0:
        print(f"\n🔥 Most mentioned species:")
        for species, count in species_counter.most_common(5):
            print(f"  • {species}: {count} mentions")

    # Save results
    if output_file is None:
        output_file = f"data/output/results_with_species.csv"

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"\n💾 Results saved to: {output_file}")

    # Save species summary
    if total_unique_species > 0:
        species_summary = pd.DataFrame([
            {'species': species, 'mention_count': count}
            for species, count in species_counter.most_common()
        ])
        summary_file = output_file.replace('.csv', '_species_summary.csv')
        species_summary.to_csv(summary_file, index=False)
        print(f"💾 Species summary saved to: {summary_file}")

def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Extract species names from literature CSV using TaxoNERD')
    parser.add_argument('input_csv', help='Path to input CSV file')
    parser.add_argument('--text-column', '-t', default='abstract',
                       help='Column name containing text to analyze (default: abstract)')
    parser.add_argument('--output', '-o', help='Output file path (optional)')

    args = parser.parse_args()

    # Check if input file exists
    if not Path(args.input_csv).exists():
        print(f"❌ Input file not found: {args.input_csv}")
        sys.exit(1)

    # Process the CSV
    process_csv(args.input_csv, args.text_column, args.output)

if __name__ == "__main__":
    main()