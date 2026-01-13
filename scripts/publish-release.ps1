# QPanels Assets - Automated Release Script
# This script handles the complete workflow: checksum calculation, commit, and push

param(
    [string]$CommitMessage = "Update QPanels Assets",
    [switch]$SkipChecksum = $false
)

$ErrorActionPreference = "Stop"

Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        QPanels Assets - Automated Release Workflow                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Get repository root
$repoRoot = $PSScriptRoot | Split-Path -Parent
Set-Location $repoRoot

Write-Host "📂 Repository: $repoRoot" -ForegroundColor White
Write-Host ""

# ============================================================================
# STEP 1: Check Git status
# ============================================================================

Write-Host "🔍 Step 1: Checking Git status..." -ForegroundColor Yellow

$gitStatus = git status --porcelain
if (-not $gitStatus -and -not $SkipChecksum) {
    Write-Host "⚠️  No changes detected. Nothing to commit." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If you want to update checksum only, use: -SkipChecksum" -ForegroundColor Gray
    exit 0
}

Write-Host "✅ Changes detected:`n" -ForegroundColor Green
git status --short
Write-Host ""

# ============================================================================
# STEP 2: Calculate SHA256 from GitHub ZIP
# ============================================================================

if (-not $SkipChecksum) {
    Write-Host "🔐 Step 2: Calculating SHA256 checksum..." -ForegroundColor Yellow
    
    # Download current main.zip from GitHub
    $tempZip = "$env:TEMP\qpanels-assets-github-$(Get-Date -Format 'yyyyMMddHHmmss').zip"
    $githubUrl = "https://github.com/lcaravella0work-prog/QPanels-Assets/archive/refs/heads/main.zip"
    
    Write-Host "  → Downloading: $githubUrl" -ForegroundColor Gray
    
    try {
        Invoke-WebRequest -Uri $githubUrl -OutFile $tempZip -UseBasicParsing
        Write-Host "  ✅ Downloaded: $tempZip" -ForegroundColor Green
        
        # Calculate SHA256
        $sha256 = (Get-FileHash -Path $tempZip -Algorithm SHA256).Hash.ToLower()
        Write-Host "  🔑 SHA256: $sha256" -ForegroundColor Cyan
        
        # Update version.json
        Write-Host "`n  → Updating version.json..." -ForegroundColor Gray
        $versionFile = Join-Path $repoRoot "version.json"
        $versionData = Get-Content $versionFile -Raw | ConvertFrom-Json
        
        if ($versionData.sha256 -eq $sha256) {
            Write-Host "  ⚠️  SHA256 unchanged. No update needed." -ForegroundColor Yellow
        } else {
            $oldSha = $versionData.sha256
            $versionData.sha256 = $sha256
            $versionData | ConvertTo-Json -Depth 10 | Set-Content $versionFile -Encoding UTF8
            Write-Host "  ✅ version.json updated" -ForegroundColor Green
            Write-Host "    Old: $oldSha" -ForegroundColor Gray
            Write-Host "    New: $sha256" -ForegroundColor Green
        }
        
        # Cleanup
        Remove-Item $tempZip -Force
        Write-Host "  🗑️  Temp file cleaned up" -ForegroundColor Gray
        
    } catch {
        Write-Host "  ❌ Error downloading or calculating checksum: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "⏭️  Step 2: Skipped (checksum calculation disabled)" -ForegroundColor Gray
}

Write-Host ""

# ============================================================================
# STEP 3: Git Add All Changes
# ============================================================================

Write-Host "📝 Step 3: Staging changes..." -ForegroundColor Yellow

git add .
$stagedCount = (git diff --cached --numstat | Measure-Object).Count

if ($stagedCount -eq 0) {
    Write-Host "  ⚠️  No changes to commit." -ForegroundColor Yellow
    exit 0
}

Write-Host "  ✅ Staged $stagedCount file(s)" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 4: Git Commit
# ============================================================================

Write-Host "💾 Step 4: Creating commit..." -ForegroundColor Yellow

# Read version from version.json
$versionFile = Join-Path $repoRoot "version.json"
$versionData = Get-Content $versionFile -Raw | ConvertFrom-Json
$version = $versionData.version

# Build commit message
$fullCommitMessage = @"
$CommitMessage

Version: $version
SHA256: $($versionData.sha256)
Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@

git commit -m $fullCommitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Commit failed!" -ForegroundColor Red
    exit 1
}

Write-Host "  ✅ Commit created" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 5: Git Push
# ============================================================================

Write-Host "🚀 Step 5: Pushing to GitHub..." -ForegroundColor Yellow

git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ Push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "  ✅ Pushed to origin/main" -ForegroundColor Green
Write-Host ""

# ============================================================================
# STEP 6: Verify Publication
# ============================================================================

Write-Host "🔍 Step 6: Verifying publication..." -ForegroundColor Yellow

Start-Sleep -Seconds 2

# Download the published ZIP to verify
$verifyZip = "$env:TEMP\qpanels-assets-verify-$(Get-Date -Format 'yyyyMMddHHmmss').zip"
$githubUrl = "https://github.com/lcaravella0work-prog/QPanels-Assets/archive/refs/heads/main.zip"

try {
    Invoke-WebRequest -Uri $githubUrl -OutFile $verifyZip -UseBasicParsing
    $publishedSha256 = (Get-FileHash -Path $verifyZip -Algorithm SHA256).Hash.ToLower()
    
    if ($publishedSha256 -eq $versionData.sha256) {
        Write-Host "  ✅ Checksum verified! Publication successful." -ForegroundColor Green
        Write-Host "    Published SHA256: $publishedSha256" -ForegroundColor Cyan
    } else {
        Write-Host "  ⚠️  Warning: Checksum mismatch (may need a few seconds to propagate)" -ForegroundColor Yellow
        Write-Host "    Expected: $($versionData.sha256)" -ForegroundColor Gray
        Write-Host "    Got:      $publishedSha256" -ForegroundColor Gray
    }
    
    Remove-Item $verifyZip -Force
    
} catch {
    Write-Host "  ⚠️  Could not verify (GitHub may still be updating)" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================================
# SUCCESS SUMMARY
# ============================================================================

Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                   🎉 Release Complete!                             ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n📦 QPanels Assets v$version published successfully!" -ForegroundColor White
Write-Host "🔗 Download: https://github.com/lcaravella0work-prog/QPanels-Assets/archive/refs/heads/main.zip" -ForegroundColor Cyan
Write-Host "🔑 SHA256: $($versionData.sha256)" -ForegroundColor Magenta
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Open Blender with QPanels Core" -ForegroundColor White
Write-Host "  2. Go to Preferences > Add-ons > QPanels > License" -ForegroundColor White
Write-Host "  3. Click 'Install QPanels Assets' or 'Check for Updates'" -ForegroundColor White
Write-Host "  4. Verify installation successful" -ForegroundColor White
Write-Host "  5. Test Outliner panel in Panel Selector (Alt+F2)" -ForegroundColor White
Write-Host ""

Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
