import os
import sys
import subprocess
import shutil
import argparse
import time

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "data", "Disciplinary cases")
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "outputs", "disciplinary")
PIPELINE_SCRIPT = os.path.join(PROJECT_ROOT, "src", "process_pipeline.py")

def main():
    parser = argparse.ArgumentParser(description="Run Disciplinary Case Batch Processing")
    parser.add_argument("--clean", action="store_true", help="Clean output directories before running")
    args = parser.parse_args()

    print(f"🚀 Starting Disciplinary Batch Processing...")
    print(f"📂 Source: {SOURCE_ROOT}")
    print(f"📂 Output: {OUTPUT_ROOT}")

    # 1. Clean Output Directory if requested
    if args.clean:
        if os.path.exists(OUTPUT_ROOT):
            print(f"🧹 Cleaning output directory: {OUTPUT_ROOT}")
            shutil.rmtree(OUTPUT_ROOT)
    
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    # 2. Find all PDFs
    pdf_files = []
    for root, dirs, files in os.walk(SOURCE_ROOT):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    # Sort for consistent processing order
    pdf_files.sort()
    print(f"📄 Found {len(pdf_files)} PDF files.")

    # 3. Process Each PDF
    success_count = 0
    fail_count = 0
    failed_files = []

    for i, pdf_path in enumerate(pdf_files):
        print(f"\n----------------------------------------------------------------")
        print(f"[{i+1}/{len(pdf_files)}] Processing: {os.path.basename(pdf_path)}")
        
        # Determine Category from folder structure
        rel_path = os.path.relpath(pdf_path, SOURCE_ROOT)
        category = os.path.dirname(rel_path)
        if category == "":
            category = "Uncategorized"
            
        # Output: OUTPUT_ROOT/<Category>/ (no subfolder per file)
        target_output_dir = os.path.join(OUTPUT_ROOT, category)
        
        print(f"  Category: {category}")
        print(f"  Target Output: {target_output_dir}")
        
        # Construct Command (force summary mode)
        cmd = [
            sys.executable,
            PIPELINE_SCRIPT,
            pdf_path,
            "--output-dir", target_output_dir,
            "--mode", "summary"
        ]
        
        start_time = time.time()
        try:
            # Run subprocess
            subprocess.run(cmd, check=True)
            duration = time.time() - start_time
            print(f"  ✅ COMPLETED in {duration:.2f}s")
            success_count += 1
        except subprocess.CalledProcessError as e:
            duration = time.time() - start_time
            print(f"  ❌ FAILED in {duration:.2f}s: {e}")
            fail_count += 1
            failed_files.append(pdf_path)
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            fail_count += 1
            failed_files.append(pdf_path)

    print("\n================================================================")
    print(f"🎉 Batch Processing Finished.")
    print(f"Total: {len(pdf_files)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")
    
    if failed_files:
        print("\nFailed Files:")
        for f in failed_files:
            print(f"- {f}")

if __name__ == "__main__":
    main()
