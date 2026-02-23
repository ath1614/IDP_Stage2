#!/usr/bin/env python3
"""
Single-command IDP pipeline for recursive folder processing.
Usage: python scripts/process_all.py <input_folder>
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from process_pipeline import main as process_document

def find_all_pdfs(root_folder):
    """Recursively find all PDF files in folder structure."""
    pdfs = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdfs.append(os.path.join(root, file))
    return pdfs

def get_output_path(pdf_path, input_root, output_root):
    """Preserve folder structure in output."""
    rel_path = os.path.relpath(os.path.dirname(pdf_path), input_root)
    output_dir = os.path.join(output_root, rel_path)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def process_all(input_folder, output_folder=None):
    """Process all PDFs in folder structure with single command."""
    
    # Default output folder
    if not output_folder:
        output_folder = os.path.join(input_folder, 'processed_output')
    
    # Find all PDFs
    print(f"Scanning {input_folder} for PDFs...")
    pdfs = find_all_pdfs(input_folder)
    
    if not pdfs:
        print("No PDF files found.")
        return
    
    print(f"Found {len(pdfs)} PDF files. Starting processing...\n")
    
    # Process each PDF
    success_count = 0
    failed_count = 0
    
    for idx, pdf_path in enumerate(pdfs, 1):
        print(f"\n{'='*80}")
        print(f"[{idx}/{len(pdfs)}] Processing: {os.path.basename(pdf_path)}")
        print(f"Path: {pdf_path}")
        print(f"{'='*80}")
        
        try:
            # Get output directory preserving structure
            output_dir = get_output_path(pdf_path, input_folder, output_folder)
            
            # Process with auto mode (classification happens inside)
            process_document(pdf_path, custom_output_dir=output_dir, mode="auto")
            
            success_count += 1
            print(f"✅ SUCCESS: {os.path.basename(pdf_path)}")
            
        except Exception as e:
            failed_count += 1
            print(f"❌ FAILED: {os.path.basename(pdf_path)}")
            print(f"Error: {str(e)}")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"Total PDFs: {len(pdfs)}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"\nOutput saved to: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process all PDFs in folder recursively")
    parser.add_argument("input_folder", help="Root folder containing PDFs")
    parser.add_argument("--output", "-o", help="Output folder (default: input_folder/processed_output)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_folder):
        print(f"Error: Folder not found: {args.input_folder}")
        sys.exit(1)
    
    process_all(args.input_folder, args.output)
