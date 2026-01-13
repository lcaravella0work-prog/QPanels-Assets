# Scripts - QPanels Assets

Automated workflow scripts for QPanels Assets development and publication.

---

## 📋 Available Scripts

### 1. `publish-release.ps1` (PowerShell - **RECOMMENDED**)

**Complete automated workflow:** Calculates SHA256 from GitHub, commits, and pushes.

**Usage:**

```powershell
# Standard release (auto-calculates checksum + commits + pushes)
.\scripts\publish-release.ps1 -CommitMessage "Add new panel feature"

# Quick commit without checksum recalculation
.\scripts\publish-release.ps1 -SkipChecksum -CommitMessage "Update documentation"
```

**What it does:**
1. ✅ Checks Git status
2. 🔐 Downloads current GitHub main.zip
3. 🔑 Calculates SHA256 checksum
4. 📝 Updates `version.json`
5. 💾 Commits changes
6. 🚀 Pushes to GitHub
7. 🔍 Verifies publication

**Exit codes:**
- `0` = Success
- `1` = Error (download failed, commit failed, or push failed)

---

### 2. `update_checksum.py` (Python - Manual workflow)

**Calculates SHA256 from GitHub** (does NOT commit/push automatically).

**Usage:**

```powershell
# From repository root
python scripts\update_checksum.py
```

**What it does:**
1. Downloads `https://github.com/.../QPanels-Assets/archive/refs/heads/main.zip`
2. Calculates SHA256
3. Updates `version.json` with new checksum
4. **You must manually commit/push**

**When to use:**
- When you want to verify checksum without committing
- When you need manual control over Git workflow

---

## 🚀 Typical Workflow

### Scenario 1: New Panel or Feature

```powershell
# 1. Develop your changes (e.g., add new panel)
# 2. Test locally

# 3. Publish automatically
cd C:\Users\<user>\Documents\GitHub\QPanels-Assets
.\scripts\publish-release.ps1 -CommitMessage "Add Node Search panel v1.0.0"

# 4. Test installation via QPanels updater in Blender
```

---

### Scenario 2: Documentation Update Only

```powershell
# 1. Update README.md or other docs

# 2. Quick publish (skip checksum recalculation)
.\scripts\publish-release.ps1 -SkipChecksum -CommitMessage "Update README with new features"
```

---

### Scenario 3: Version Bump

```powershell
# 1. Manually edit version.json (increment version: 1.0.0 → 1.1.0)

# 2. Update changelog in version.json

# 3. Publish with new version
.\scripts\publish-release.ps1 -CommitMessage "Release v1.1.0 - Add Node Search panel"
```

---

## 🔧 Manual Git Workflow (Without Scripts)

If you prefer manual control:

```powershell
cd C:\Users\<user>\Documents\GitHub\QPanels-Assets

# 1. Calculate checksum
python scripts\update_checksum.py

# 2. Stage changes
git add .

# 3. Commit
git commit -m "Your commit message"

# 4. Push
git push origin main
```

---

## ⚠️ Important Notes

### SHA256 Checksum Source

**Always calculate from GitHub ZIP**, not local files!

**Why?** GitHub's ZIP format includes metadata (timestamps, Git info) that differs from locally created ZIPs.

**Correct workflow:**
1. Commit/push your changes
2. Download `archive/refs/heads/main.zip` from GitHub
3. Calculate SHA256 from that ZIP
4. Update `version.json` with that SHA256
5. Commit/push the version.json update

**Our scripts handle this automatically!**

---

### Git Configuration

Ensure your Git credentials are configured:

```powershell
# Check current config
git config user.name
git config user.email

# Set if needed
git config user.name "Your Name"
git config user.email "your.email@example.com"

# For SSH authentication (recommended)
# Ensure SSH key is added to GitHub account
```

---

## 📊 Script Comparison

| Feature | `publish-release.ps1` | `update_checksum.py` |
|---------|----------------------|---------------------|
| **Language** | PowerShell | Python |
| **Calculates SHA256** | ✅ (from GitHub) | ✅ (from GitHub) |
| **Updates version.json** | ✅ Auto | ✅ Auto |
| **Git commit** | ✅ Auto | ❌ Manual |
| **Git push** | ✅ Auto | ❌ Manual |
| **Verification** | ✅ Auto | ❌ Manual |
| **Use case** | Full automation | Manual control |

---

## 🛠️ Troubleshooting

### Error: "Push failed"

**Possible causes:**
- No Git credentials configured
- Network issue
- Merge conflict

**Solution:**

```powershell
# Check remote
git remote -v

# Pull latest changes
git pull origin main

# Resolve conflicts if any, then re-run script
```

---

### Error: "Checksum mismatch"

**Cause:** GitHub may still be propagating changes (takes 5-10 seconds).

**Solution:** Wait 10 seconds and re-run verification:

```powershell
python scripts\update_checksum.py
git add version.json
git commit -m "Update checksum"
git push origin main
```

---

### Error: "Download failed"

**Possible causes:**
- Network issue
- GitHub API rate limit
- Repository private/inaccessible

**Solution:**
- Check internet connection
- Verify repository is public
- Wait a few minutes (rate limit resets)

---

## 📝 Examples

### Example 1: First Release

```powershell
# Navigate to repository
cd C:\Users\lcara\Documents\GitHub\QPanels-Assets

# Create initial commit
git add .
git commit -m "Initial commit - QPanels Assets v1.0.0"
git push origin main

# Calculate checksum from GitHub
python scripts\update_checksum.py

# Commit checksum update
git add version.json
git commit -m "Add SHA256 checksum"
git push origin main
```

---

### Example 2: Subsequent Releases (Automated)

```powershell
# Make changes (add panel, fix bug, etc.)

# Publish automatically
.\scripts\publish-release.ps1 -CommitMessage "Add Animation Helper panel v1.0.0"

# Done! Script handles everything
```

---

### Example 3: Hotfix

```powershell
# Fix critical bug in outliner/ui.py

# Quick publish
.\scripts\publish-release.ps1 -CommitMessage "Hotfix: Fix outliner crash on empty collection"
```

---

## 🔗 Related Documentation

- [QPANELS_ASSETS_ARCHITECTURE.md](../../QPanels-Core/docs/QPANELS_ASSETS_ARCHITECTURE.md) - Complete architecture guide
- [README.md](../README.md) - User documentation
- [CHANGELOG.md](../CHANGELOG.md) - Version history

---

**Last Updated:** 2026-01-13  
**Scripts Version:** 1.0.0
