# QPanels Assets - Guide de Publication

## Vue d'ensemble

Ce guide explique comment publier une nouvelle version de QPanels Assets sur GitHub Releases en utilisant le système automatisé.

## Architecture GitHub Releases

### Problème résolu

**Avant** : Le système utilisait `archive/refs/heads/main.zip`, dont le SHA256 changeait à chaque commit (même sans modification de contenu), rendant impossible la validation d'intégrité.

**Maintenant** : GitHub Releases avec tags versionnés. Le ZIP est immuable et exclu `version.json`, permettant un SHA256 stable.

### Workflow complet

```
Développeur modifie panels/
    ↓
.\publish-assets.ps1 -Type patch
    ↓
[1] Parse version actuelle (version.json)
[2] Incrémente version (1.0.0 → 1.0.1)
[3] Build ZIP (SANS version.json)
[4] Calcul SHA256 du ZIP
[5] Update version.json avec download_url + SHA256
[6] Git commit + push
[7] Create GitHub Release (tag v1.0.1)
[8] Upload ZIP asset
[9] Validation (download + verify SHA256)
    ↓
Utilisateurs installent via QPanels Core → Install Assets
```

## Prérequis

### 1. Token GitHub

Créer un Personal Access Token :
1. Aller sur : https://github.com/settings/tokens/new
2. Nom : "QPanels Assets Publisher"
3. Scopes requis :
   - ✅ `repo` (Full control of private repositories)
4. Copier le token : `ghp_...`

### 2. Configurer le token

**Option A - Variable d'environnement** (recommandé) :
```powershell
$env:GITHUB_TOKEN = "ghp_votre_token_ici"
```

**Option B - Paramètre** :
```powershell
.\publish-assets.ps1 -GitHubToken "ghp_votre_token_ici" -Type patch
```

## Utilisation

### Commandes principales

#### Publier patch (bugfix)
```powershell
# 1.0.0 → 1.0.1
.\publish-assets.ps1 -Type patch
```

#### Publier minor (nouvelle fonctionnalité)
```powershell
# 1.0.1 → 1.1.0
.\publish-assets.ps1 -Type minor
```

#### Publier major (breaking change)
```powershell
# 1.1.0 → 2.0.0
.\publish-assets.ps1 -Type major
```

#### Forcer version spécifique
```powershell
.\publish-assets.ps1 -Version "1.5.0"
```

#### Mode simulation (DryRun)
```powershell
# Teste sans publier
.\publish-assets.ps1 -Type patch -DryRun
```

### Exemples concrets

#### Scénario 1 : Bugfix dans Outliner panel

```powershell
# Contexte : Fix crash quand collection vide
# Version actuelle : 1.0.0

cd C:\Users\...\QPanels-Assets
git add panels/outliner/
git commit -m "Fix crash on empty collection"

# Publier patch
$env:GITHUB_TOKEN = "ghp_..."
.\publish-assets.ps1 -Type patch

# Résultat : v1.0.1 publié sur GitHub Releases
```

#### Scénario 2 : Nouveau panel (Node Search)

```powershell
# Contexte : Ajout Node Search panel
# Version actuelle : 1.0.1

cd C:\Users\...\QPanels-Assets
git add panels/node_search/
git commit -m "Add Node Search panel"

# Publier minor
.\publish-assets.ps1 -Type minor

# Résultat : v1.1.0 publié
```

#### Scénario 3 : Refonte architecture panels

```powershell
# Contexte : Breaking change dans panels/__init__.py
# Version actuelle : 1.1.0

cd C:\Users\...\QPanels-Assets
git add panels/
git commit -m "BREAKING: Refactor panels registration system"

# Publier major
.\publish-assets.ps1 -Type major

# Résultat : v2.0.0 publié
```

## Workflow recommandé

### 1. Développement local

```powershell
# Modifier le code
code panels/outliner/operators.py

# Tester localement
# (copier manuellement dans Blender addons/)

# Commit changes
git add .
git commit -m "Fix: RTO toggle not working"
git push origin main
```

### 2. Publication

```powershell
# Publier release
.\publish-assets.ps1 -Type patch

# Output attendu :
# [VALIDATION]
# [PARSE VERSION]
# [CALCULATE NEW VERSION]
#   Current: 1.0.0 -> New: 1.0.1
# [BUILD ZIP]
#   ZIP created: 29.34 KB
# [CALCULATE SHA256]
#   SHA256: 0b4dffbd17...
# [UPDATE version.json]
# [GIT COMMIT]
#   Pushed to GitHub
# [CREATE GITHUB RELEASE]
#   Release created: https://github.com/.../releases/tag/v1.0.1
# [UPLOAD ZIP]
#   Asset uploaded: https://github.com/.../qpanel-assets-v1.0.1.zip
# [VALIDATE]
#   SHA256 validated
# [SUCCESS] QPanels Assets v1.0.1 published!
```

### 3. Vérification

1. **GitHub UI** :
   - Aller sur : https://github.com/lcaravella0work-prog/QPanels-Assets/releases
   - Vérifier que v1.0.1 apparaît
   - Télécharger le ZIP pour tester

2. **Blender** :
   - Ouvrir Blender
   - QPanels → Preferences → License
   - Cliquer "Install QPanels Assets"
   - Vérifier logs :
     ```
     [QPanel Assets] Using GitHub Releases download
     [QPanel Assets] Download progress: 100%
     [QPanel Assets] ✓ Checksum verified
     [QPanel Assets] Installation complete!
     ```

## Structure de version.json

Après publication, `version.json` contient :

```json
{
  "version": "1.0.1",
  "download_url": "https://github.com/.../releases/download/v1.0.1/qpanel-assets-v1.0.1.zip",
  "sha256": "0b4dffbd175762f3eefd3bab78ba51eb411eaef54b2f0fd43e9c2501ee028fd5",
  "size": 30041,
  "blender_min_version": "3.4.0",
  "qpanels_min_version": "6.2.0",
  "changelog": "Initial release with Outliner panel",
  "panels": [...]
}
```

**Important** :
- `download_url` : URL de la release GitHub (immuable)
- `sha256` : Hash du ZIP de la release (stable)
- `size` : Taille en bytes

## Gestion des erreurs

### Erreur : Tag already exists

```
fatal: tag 'v1.0.0' already exists
```

**Solution** : Le tag existe déjà. Incrémenter la version :
```powershell
.\publish-assets.ps1 -Type patch  # Créera v1.0.1
```

### Erreur : GitHub token required

```
GitHub token required. Set $env:GITHUB_TOKEN or use -GitHubToken
```

**Solution** :
```powershell
$env:GITHUB_TOKEN = "ghp_votre_token"
```

### Erreur : SHA256 mismatch

```
SHA256 mismatch! Expected: abc..., Got: def...
```

**Cause** : Erreur réseau pendant upload

**Solution automatique** : Le script exécute un rollback :
1. Supprime tag local et remote
2. Supprime GitHub Release
3. Restore version.json

**Action** : Re-lancer `.\publish-assets.ps1`

### Erreur : Rate limit exceeded

```
Rate limit exceeded. Waiting 3600 seconds...
```

**Cause** : GitHub API limit (60 req/h sans auth, 5000/h avec token)

**Solution** : Attendre ou utiliser token authentifié

## Rollback manuel

Si la publication échoue et que le rollback automatique ne fonctionne pas :

```powershell
# 1. Supprimer tag local
git tag -d v1.0.1

# 2. Supprimer tag remote
git push origin --delete v1.0.1

# 3. Restaurer version.json
git checkout HEAD~1 -- version.json
git add version.json
git commit -m "Rollback failed release v1.0.1"
git push origin main

# 4. Supprimer release GitHub (UI)
# https://github.com/.../QPanels-Assets/releases
# → Delete release
```

## Changelog automatique

Le script génère un changelog basique depuis les commits Git :

```powershell
# Commits depuis dernier tag
$lastTag = git describe --tags --abbrev=0
$commits = git log $lastTag..HEAD --oneline --no-merges

# Output dans release notes
- Fix crash on empty collection
- Update README.md
- Add tests for outliner panel
```

**Amélioration future** : Parser Conventional Commits (`feat:`, `fix:`, `BREAKING:`)

## Intégration avec QPanels Core

### Comment Core télécharge les Assets

1. **Fetch version.json** :
   ```python
   # URL : https://raw.githubusercontent.com/.../main/version.json
   remote_version = get_remote_version()
   ```

2. **Lire download_url** :
   ```python
   download_url = remote_version.get('download_url')
   # GitHub Releases : .../releases/download/v1.0.1/qpanel-assets-v1.0.1.zip
   ```

3. **Download + Verify** :
   ```python
   expected_sha256 = remote_version.get('sha256')
   download_assets(download_url, temp_zip, expected_sha256)
   ```

### Fallback legacy

Si `download_url` absent dans `version.json` (anciennes versions) :

```python
if not download_url:
    # Fallback vers archive/main.zip (sans SHA256 validation)
    download_url = "https://github.com/.../archive/refs/heads/main.zip"
```

## Maintenance

### Vérifier releases existantes

```powershell
# Via GitHub API
$headers = @{ "Authorization" = "Bearer $env:GITHUB_TOKEN" }
$releases = Invoke-RestMethod -Uri "https://api.github.com/repos/lcaravella0work-prog/QPanels-Assets/releases" -Headers $headers

$releases | Select-Object tag_name, name, created_at, assets
```

### Supprimer ancienne release

```powershell
# Via UI : https://github.com/.../releases
# → Delete release (garde le tag Git)

# Supprimer aussi le tag :
git tag -d v1.0.0
git push origin --delete v1.0.0
```

### Statistiques téléchargements

GitHub Insights → Traffic → Git clones / Downloads

## Support

### Logs de publication

Le script affiche tous les détails :
- Version calculée
- Taille du ZIP
- SHA256
- URLs GitHub
- Validation post-upload

### Debug mode

Ajouter `-Verbose` pour détails supplémentaires :
```powershell
.\publish-assets.ps1 -Type patch -Verbose
```

### Contact

- Issues : https://github.com/lcaravella0work-prog/QPanels-Assets/issues
- Email : l.caravella0.work@gmail.com

---

**Dernière mise à jour** : 13 janvier 2026  
**Version du guide** : 1.0
