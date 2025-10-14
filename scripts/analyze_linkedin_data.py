# scripts/analyze_linkedin_data.py

import os
import pandas as pd

# --- Configuration ---
DATA_SOURCES_PATH = '../data_sources/'
OUTPUT_FILENAME = '../linkedin_data_analysis.md' # Output file will be in the project's root folder

def analyze_csv_files_to_markdown(path, output_filepath):
    """
    Scans a directory for CSV files and writes a detailed analysis
    to a Markdown file.
    """
    print(f"--- Starting Analysis of CSVs in '{path}' ---")

    try:
        files = os.listdir(path)
    except FileNotFoundError:
        print(f"ERROR: Directory not found: '{path}'")
        return

    csv_files = [f for f in files if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    # Use a 'with' statement to safely open and write to the file
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write("# LinkedIn Data Export Analysis\n\n")
        f.write("This document contains an automated analysis of all CSV files found in the LinkedIn data export.\n\n")

        for filename in sorted(csv_files):
            file_path = os.path.join(path, filename)
            
            # Write the header for each file in Markdown format
            f.write(f"## Analysis for: `{filename}`\n\n")

            try:
                df = pd.read_csv(file_path)

                # Write Shape
                f.write(f"**Shape:** {df.shape[0]} rows, {df.shape[1]} columns\n\n")

                # Write Schema (Column Names)
                f.write("**Schema (Column Names):**\n")
                f.write("```\n")
                f.write(f"{df.columns.tolist()}\n")
                f.write("```\n\n")

                # Write Sample Data
                f.write("**Sample Data (First 3 Rows):**\n")
                if not df.empty:
                    f.write("```text\n")
                    # Use to_string() to prevent pandas from truncating the output
                    f.write(df.head(3).to_string())
                    f.write("\n```\n\n")
                else:
                    f.write("`This file is empty.`\n\n")

            except Exception as e:
                f.write(f"**Error:** Could not process this file. Reason: `{e}`\n\n")
            
            f.write("---\n\n") # Add a horizontal rule for separation

    print(f"--- Analysis Complete! ---")
    print(f"Report has been saved to: {output_filepath}")

if __name__ == '__main__':
    analyze_csv_files_to_markdown(DATA_SOURCES_PATH, OUTPUT_FILENAME)