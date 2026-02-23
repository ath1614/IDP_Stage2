import os
import shutil
import argparse

def flatten_apar_directory(target_dir):
    """
    Flattens the directory structure for APAR documents.
    Structure: Root/Subfolder/File -> Root/File
    """
    print(f"📂 Processing: {target_dir}")
    
    # Walk through the root folder
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for file in files:
            # We are looking for any file inside subfolders, not just .docx if they exist
            # But the request specifically mentioned docx context, but let's be safe and move everything
            # or stick to docx if that's the only thing expected. 
            # Given previous context "similarly for apar documents", I'll move everything.
            
            source_path = os.path.join(root, file)
            
            # If the file is already in the root, skip it
            if root == target_dir:
                continue
                
            # Target path is directly under the root folder
            dest_path = os.path.join(target_dir, file)
            
            # Handle name collisions
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(file)
                dest_path = os.path.join(target_dir, f"{base}_moved{ext}")
            
            print(f"    📦 Moving {file} -> {target_dir}/")
            shutil.move(source_path, dest_path)
        
        # Remove empty directories (except root)
        if root != target_dir:
            try:
                os.rmdir(root)
                print(f"    🗑️  Removed empty dir: {os.path.basename(root)}")
            except OSError:
                pass # Directory not empty

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten APAR output structure")
    parser.add_argument("--dir", default="/Users/atharvsoni/IDP2/apar_output", help="Target directory")
    args = parser.parse_args()
    
    if os.path.exists(args.dir):
        flatten_apar_directory(args.dir)
        print("✅ Flattening complete.")
    else:
        print(f"❌ Directory not found: {args.dir}")
