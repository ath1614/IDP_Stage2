import os
import sys
import subprocess
import shutil
import argparse
import time

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Default generic data folder or specific APAR folder
SOURCE_ROOT = os.path.join(PROJECT_ROOT, "data") 
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "outputs", "apar")
PIPELINE_SCRIPT = os.path.join(PROJECT_ROOT, "src", "process_pipeline.py")

def main():
    parser = argparse.ArgumentParser(description="Run APAR Batch Processing")
    parser.add_argument("--source", help="Path to folder containing APAR PDFs (default: data/)", default=SOURCE_ROOT)
    parser.add_argument("--clean", action="store_true", help="Clean output directory before running")
    args = parser.parse_args()

    source_dir = args.source
    
    print(f"🚀 Starting APAR Batch Processing...")
    print(f"📂 Source: {source_dir}")
    print(f"📂 Output: {OUTPUT_ROOT}")

    # 1. Clean Output Directory if requested
    if args.clean:
        if os.path.exists(OUTPUT_ROOT):
            print(f"🧹 Cleaning output directory: {OUTPUT_ROOT}")
            shutil.rmtree(OUTPUT_ROOT)
    
    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    # 2. Find all APAR PDFs (heuristic: filename contains 'APAR')
    pdf_files = []
    if os.path.isdir(source_dir):
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith('.pdf') and "apar" in file.lower():
                    pdf_files.append(os.path.join(root, file))
    else:
        print(f"❌ Source directory not found: {source_dir}")
        return

    # Sort
    pdf_files.sort()
    print(f"📄 Found {len(pdf_files)} potential APAR files.")

    # 3. Process Each PDF
    success_count = 0
    fail_count = 0
    failed_files = []

    for i, pdf_path in enumerate(pdf_files):
        print(f"\n----------------------------------------------------------------")
        print(f"[{i+1}/{len(pdf_files)}] Processing: {os.path.basename(pdf_path)}")
        
        # Output directly to OUTPUT_ROOT (no subfolder)
        print(f"  Target Output: {OUTPUT_ROOT}")
        
        # Construct Command (force apar mode)
        cmd = [
            sys.executable,
            PIPELINE_SCRIPT,
            pdf_path,
            "--output-dir", OUTPUT_ROOT,
            "--mode", "apar"
        ]
        
        start_time = time.time()
        try:
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
    print(f"🎉 APAR Batch Processing Finished.")
    print(f"Total: {len(pdf_files)}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")

if __name__ == "__main__":
    main()
