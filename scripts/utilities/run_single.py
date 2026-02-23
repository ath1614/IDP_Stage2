import os
import sys
import subprocess
import argparse
import time

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE_SCRIPT = os.path.join(PROJECT_ROOT, "src", "process_pipeline.py")

def main():
    parser = argparse.ArgumentParser(description="Run Pipeline for a Single File")
    parser.add_argument("file_path", help="Path to the PDF file")
    parser.add_argument("--output-dir", help="Custom output directory")
    parser.add_argument("--mode", default="auto", choices=["auto", "apar", "summary"], help="Processing mode")
    args = parser.parse_args()

    file_path = os.path.abspath(args.file_path)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    # Default output dir if not specified: outputs/single_runs/<filename>/
    if not args.output_dir:
        filename = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.join(PROJECT_ROOT, "outputs", "single_runs", filename)
    else:
        output_dir = os.path.abspath(args.output_dir)

    print(f"🚀 Processing Single File: {file_path}")
    print(f"📂 Output: {output_dir}")
    print(f"⚙️  Mode: {args.mode}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    cmd = [
        sys.executable,
        PIPELINE_SCRIPT,
        file_path,
        "--output-dir", output_dir,
        "--mode", args.mode
    ]
    
    try:
        start_time = time.time()
        subprocess.run(cmd, check=True)
        duration = time.time() - start_time
        print(f"✅ COMPLETED in {duration:.2f}s")
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
