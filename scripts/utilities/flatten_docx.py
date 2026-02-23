import os
import shutil
import argparse

def flatten_directory(target_dir):
    """
    Flattens the directory structure by moving files from subfolders to the category folder.
    Structure: Root/Category/Subfolder/File -> Root/Category/File
    """
    print(f"📂 Processing: {target_dir}")
    
    # Get the list of categories (first level subdirectories)
    categories = [d for d in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, d))]
    
    for category in categories:
        category_path = os.path.join(target_dir, category)
        print(f"  🔹 Category: {category}")
        
        # Walk through the category folder
        for root, dirs, files in os.walk(category_path, topdown=False):
            for file in files:
                if file.lower().endswith('.docx'):
                    source_path = os.path.join(root, file)
                    
                    # If the file is already in the category root, skip it
                    if root == category_path:
                        continue
                        
                    # Target path is directly under the category folder
                    dest_path = os.path.join(category_path, file)
                    
                    # Handle name collisions
                    if os.path.exists(dest_path):
                        base, ext = os.path.splitext(file)
                        dest_path = os.path.join(category_path, f"{base}_moved{ext}")
                    
                    print(f"    📦 Moving {file} -> {category}/")
                    shutil.move(source_path, dest_path)
            
            # Remove empty directories
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                    print(f"    🗑️  Removed empty dir: {dir_name}")
                except OSError:
                    pass # Directory not empty

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flatten DOCX output structure")
    parser.add_argument("--dir", default="/Users/atharvsoni/IDP2/disciplinary cases docx", help="Target directory")
    args = parser.parse_args()
    
    if os.path.exists(args.dir):
        flatten_directory(args.dir)
        print("✅ Flattening complete.")
    else:
        print(f"❌ Directory not found: {args.dir}")
