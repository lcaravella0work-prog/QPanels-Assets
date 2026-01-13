"""
Update SHA256 Checksum for QPanels Assets
Calculates SHA256 of the package and updates version.json
"""

import hashlib
import json
import zipfile
import os
from pathlib import Path

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_package_zip(source_dir, output_path):
    """Create ZIP package of QPanels Assets."""
    print(f"Creating package: {output_path}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Skip certain directories
            skip_dirs = {'.git', '__pycache__', '.vscode', 'scripts'}
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                # Skip certain files
                if file.endswith(('.pyc', '.pyo', '.git', '.gitignore')):
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                print(f"  Adding: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"✅ Package created: {output_path}")

def update_version_json(version_file, sha256_hash):
    """Update version.json with new SHA256 hash."""
    print(f"\nUpdating version.json...")
    
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)
    
    version_data['sha256'] = sha256_hash
    
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ version.json updated with SHA256: {sha256_hash}")

def main():
    """Main workflow: Create ZIP → Calculate SHA256 → Update version.json"""
    
    # Paths
    repo_root = Path(__file__).parent.parent
    package_dir = repo_root
    temp_zip = repo_root.parent / "qpanel-assets-temp.zip"
    version_file = repo_root / "version.json"
    
    print("=" * 60)
    print("QPanels Assets - SHA256 Update Script")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"Package ZIP: {temp_zip}")
    print(f"Version file: {version_file}")
    print("=" * 60)
    
    # Step 1: Create package ZIP
    create_package_zip(package_dir, temp_zip)
    
    # Step 2: Calculate SHA256
    print(f"\nCalculating SHA256 hash...")
    sha256_hash = calculate_sha256(temp_zip)
    print(f"SHA256: {sha256_hash}")
    
    # Step 3: Update version.json
    update_version_json(version_file, sha256_hash)
    
    # Step 4: Cleanup temp ZIP
    print(f"\nCleaning up temporary files...")
    temp_zip.unlink()
    print(f"✅ Removed: {temp_zip}")
    
    print("\n" + "=" * 60)
    print("✅ SHA256 update complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review changes in version.json")
    print("2. Commit and push to GitHub")
    print("3. QPanels will detect the new version")
    print("=" * 60)

if __name__ == "__main__":
    main()
