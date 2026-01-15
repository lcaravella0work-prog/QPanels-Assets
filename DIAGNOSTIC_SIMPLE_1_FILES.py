"""
🔍 DIAGNOSTIC 1 - Vérification fichiers (SAFE - Ne crash pas Blender)

UTILISATION:
1. Ouvrir Blender avec QPanels installé
2. Scripting > Text Editor > Open
3. Charger ce fichier
4. Run Script (Alt+P)
5. Lire résultats dans Console
"""

from pathlib import Path
import bpy

print("\n" + "="*80)
print("🔍 DIAGNOSTIC 1 - Vérification installation fichiers")
print("="*80 + "\n")

# Chemin Assets
scripts_addons = Path(bpy.utils.user_resource('SCRIPTS')) / "addons"
assets_dir = scripts_addons / "qpanel_assets"

print(f"📁 Dossier Assets: {assets_dir}")
print(f"   Existe: {assets_dir.exists()}\n")

if not assets_dir.exists():
    print("❌ qpanel_assets/ n'existe pas - pas installé")
else:
    # Lister tous les fichiers
    print("📂 Structure:")
    
    def show_tree(path, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                marker = "└── " if is_last else "├── "
                print(f"{prefix}{marker}{item.name}{'/' if item.is_dir() else ''}")
                
                if item.is_dir() and not item.name.startswith('__pycache__'):
                    extension = "    " if is_last else "│   "
                    show_tree(item, prefix + extension, max_depth, current_depth + 1)
        except PermissionError:
            pass
    
    show_tree(assets_dir)
    
    # Fichiers requis
    print("\n✅ Fichiers critiques:")
    required = {
        "version.json": assets_dir / "version.json",
        "__init__.py": assets_dir / "__init__.py",
        "panels/": assets_dir / "panels",
        "panels/__init__.py": assets_dir / "panels" / "__init__.py",
        "panels/outliner/": assets_dir / "panels" / "outliner",
        "panels/outliner/__init__.py": assets_dir / "panels" / "outliner" / "__init__.py",
        "panels/outliner/ui.py": assets_dir / "panels" / "outliner" / "ui.py",
        "panels/outliner/operators.py": assets_dir / "panels" / "outliner" / "operators.py",
    }
    
    all_ok = True
    for name, path in required.items():
        exists = path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {name}")
        if not exists:
            all_ok = False
    
    if all_ok:
        print("\n✅ Tous les fichiers requis sont présents!")
    else:
        print("\n❌ Des fichiers sont manquants - réinstaller QPanels Assets")

print("\n" + "="*80)
print("FIN DIAGNOSTIC 1")
print("="*80 + "\n")
