"""
Update SHA256 Checksum for QPanels Assets
Downloads the actual GitHub ZIP and calculates its SHA256
"""

import hashlib
import json
import urllib.request
import tempfile
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

def download_github_zip(url, output_path):
    """Download ZIP from GitHub."""
    print(f"Downloading from GitHub: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(output_path, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='\r')
        
        print(f"\n✅ Download complete: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

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
    """Main workflow: Download GitHub ZIP → Calculate SHA256 → Update version.json"""
    
    # Paths
    repo_root = Path(__file__).parent.parent
    version_file = repo_root / "version.json"
    
    # GitHub URL for main.zip
    github_url = "https://github.com/lcaravella0work-prog/QPanels-Assets/archive/refs/heads/main.zip"
    
    # Temporary file for download
    temp_zip = tempfile.mktemp(suffix='.zip', prefix='qpanels-assets-')
    
    print("=" * 60)
    print("QPanels Assets - SHA256 Update Script")
    print("=" * 60)
    print(f"Repository: {repo_root}")
    print(f"GitHub URL: {github_url}")
    print(f"Version file: {version_file}")
    print("=" * 60)
    
    try:
        # Step 1: Download GitHub ZIP
        if not download_github_zip(github_url, temp_zip):
            print("\n❌ Failed to download GitHub ZIP")
            return
        
        # Step 2: Calculate SHA256
        print(f"\nCalculating SHA256 hash...")
        sha256_hash = calculate_sha256(temp_zip)
        print(f"SHA256: {sha256_hash}")
        
        # Step 3: Update version.json
        update_version_json(version_file, sha256_hash)
        
        print("\n" + "=" * 60)
        print("✅ SHA256 update complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review changes in version.json")
        print("2. Run: git add version.json")
        print("3. Run: git commit -m 'Update SHA256 checksum'")
        print("4. Run: git push origin main")
        print("=" * 60)
        
    finally:
        # Cleanup temp file
        if os.path.exists(temp_zip):
            os.unlink(temp_zip)
            print(f"\n🗑️  Cleaned up: {temp_zip}")

if __name__ == "__main__":
    main()
