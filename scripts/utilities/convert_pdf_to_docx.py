import os
import argparse
from pdf2docx import Converter
import sys
import shutil

def convert_pdf_to_docx(pdf_file, docx_file):
    """
    Convert a single PDF file to DOCX.
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(docx_file), exist_ok=True)
        
        print(f"🔄 Converting: {pdf_file} -> {docx_file}")
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()
        print(f"✅ Created: {docx_file}")
        return True
    except Exception as e:
        print(f"❌ Error converting {pdf_file}: {e}")
        return False

def process_directory(source_dir, output_dir=None):
    """
    Recursively find all PDF files in source_dir and convert them to DOCX.
    If output_dir is provided, mirrors the structure.
    If output_dir is None, saves in the same directory.
    """
    print(f"📂 Scanning directory: {source_dir}")
    if output_dir:
        print(f"📂 Output directory: {output_dir}")
    
    pdf_files = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    if not pdf_files:
        print("⚠️ No PDF files found.")
        return

    print(f"📄 Found {len(pdf_files)} PDF files.")
    
    success_count = 0
    for pdf_path in pdf_files:
        if output_dir:
            # Calculate relative path to mirror structure
            rel_path = os.path.relpath(pdf_path, source_dir)
            # Change extension
            rel_path_docx = os.path.splitext(rel_path)[0] + ".docx"
            docx_path = os.path.join(output_dir, rel_path_docx)
        else:
            docx_path = os.path.splitext(pdf_path)[0] + ".docx"
        
        if convert_pdf_to_docx(pdf_path, docx_path):
            success_count += 1
            
    print(f"🎉 Conversion complete. {success_count}/{len(pdf_files)} files converted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert all PDF files in a directory to DOCX.")
    parser.add_argument("--input", help="Input directory to scan for PDFs", required=True)
    parser.add_argument("--output", help="Output directory for DOCX files (mirrors structure)", required=False)
    
    args = parser.parse_args()
    
    source_dir = args.input
    output_dir = args.output
    
    if not os.path.exists(source_dir):
        print(f"❌ Source directory not found: {source_dir}")
        sys.exit(1)
        
    process_directory(source_dir, output_dir)
