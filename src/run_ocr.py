import fitz  # pymupdf
import requests
import base64
import sys
import io
import argparse
import os
from PIL import Image

def pdf_to_base64_images(pdf_path):
    doc = fitz.open(pdf_path)
    images_b64 = []
    
    print(f"Processing PDF: {pdf_path} ({len(doc)} pages)", flush=True)
    
    for i, page in enumerate(doc):
        # Higher DPI for better OCR accuracy
        pix = page.get_pixmap(dpi=200) 
        img_data = pix.tobytes("png")
        
        b64_str = base64.b64encode(img_data).decode('utf-8')
        images_b64.append(b64_str)
        print(f"  Page {i+1} converted to image.", flush=True)
        
    return images_b64

def run_ocr(pdf_path, service_url, output_file):
    try:
        images = pdf_to_base64_images(pdf_path)
        
        if not images:
            print("No images extracted from PDF.")
            return

        # Prepare payload
        payload = {
            "images": images,
            "languages": ["en"] # Defaulting to English
        }
        
        print(f"Sending {len(images)} images to OCR service at {service_url}...")
        
        # Add timeout for large files (120s)
        response = requests.post(f"{service_url}/api/ocr/batch", json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("\n--- OCR Completed ---\n")
            
            full_text = []
            
            for i, res in enumerate(result.get("results", [])):
                page_text = res.get("text", "")
                confidence = res.get("confidence", 0)
                
                # Format for output file
                page_content = f"--- Page {i+1} (Confidence: {confidence:.2f}) ---\n{page_text}\n\n"
                full_text.append(page_content)
                
                # Print preview to console (first 100 chars)
                print(f"Page {i+1}: {page_text[:100]}...")

            # Save to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("".join(full_text))
            
            print(f"\nFull extracted text saved to: {output_file}")
            print(f"Total processing time: {result.get('processing_time_ms', 0)}ms")
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load environment variables
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(project_root, ".env"))
    
    default_ocr_ip = os.getenv("OCR_VM_IP", "34.47.176.38")
    default_ocr_url = f"http://{default_ocr_ip}:8000"

    parser = argparse.ArgumentParser(description="Run OCR on a PDF using remote or local service")
    parser.add_argument("input_pdf", help="Path to the PDF file")
    parser.add_argument("--url", default=default_ocr_url, help=f"URL of the OCR service (default: {default_ocr_url})")
    parser.add_argument("--output", help="Output text file path")
    
    args = parser.parse_args()
    
    # Determine output filename if not provided
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.input_pdf))[0]
        args.output = f"{base_name}_extracted.txt"
    
    run_ocr(args.input_pdf, args.url, args.output)
