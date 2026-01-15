"""
🔍 DIAGNOSTIC QPANEL ASSETS - Script à exécuter dans Blender Console

UTILISATION:
1. Ouvrir Blender avec QPanels installé
2. Aller dans Scripting > Text Editor > Open
3. Charger ce fichier DIAGNOSTIC_BLENDER.py
4. Cliquer "Run Script" (ou Alt+P)
5. Lire les résultats dans la Console

Ce script vérifie:
- Installation des fichiers Assets
- Import du module panels
- Enregistrement des classes Blender
- Disponibilité du panel Outliner
- Opérateurs accessibles
"""

import sys
import bpy
from pathlib import Path

print("\n" + "="*80)
print("🔍 DIAGNOSTIC QPANEL ASSETS - v2.1.1")
print("="*80 + "\n")

# =============== 1. VÉRIFICATION INSTALLATION ===============
print("📁 ÉTAPE 1: Vérification installation fichiers")
print("-" * 80)

# Chemin AppData Blender
blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
scripts_addons = Path(bpy.utils.user_resource('SCRIPTS')) / "addons"
assets_dir = scripts_addons / "qpanel_assets"

print(f"Dossier Blender: {scripts_addons}")
print(f"Assets dir: {assets_dir}")
print(f"Existe: {assets_dir.exists()}")

if not assets_dir.exists():
    print("❌ ERREUR: qpanel_assets/ n'existe pas!")
    print("   → L'installation n'a pas créé le dossier")
    sys.exit(1)

# Vérifier fichiers requis
required_files = {
    "version.json": assets_dir / "version.json",
    "__init__.py": assets_dir / "__init__.py",
    "panels/__init__.py": assets_dir / "panels" / "__init__.py",
    "panels/outliner/__init__.py": assets_dir / "panels" / "outliner" / "__init__.py",
    "panels/outliner/ui.py": assets_dir / "panels" / "outliner" / "ui.py",
}

print("\nFichiers requis:")
all_present = True
for name, path in required_files.items():
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {name}: {path}")
    if not exists:
        all_present = False

if not all_present:
    print("\n❌ ERREUR: Fichiers manquants!")
    print("   → Le ZIP n'a pas été extrait correctement")
    sys.exit(1)

print("\n✅ Tous les fichiers requis sont présents")

# =============== 2. VÉRIFICATION IMPORT MODULE ===============
print("\n📦 ÉTAPE 2: Test import module panels")
print("-" * 80)

# Ajouter au sys.path
if str(assets_dir) not in sys.path:
    sys.path.insert(0, str(assets_dir))
    print(f"✅ Ajouté au sys.path: {assets_dir}")

# Test import
try:
    import panels
    print("✅ Import panels réussi")
    
    # Vérifier sous-modules
    if hasattr(panels, 'outliner'):
        print("✅ Sous-module panels.outliner trouvé")
        
        # Lister les classes disponibles
        print("\n  Classes disponibles dans panels.outliner:")
        for attr_name in dir(panels.outliner):
            attr = getattr(panels.outliner, attr_name)
            if isinstance(attr, type) and hasattr(attr, 'bl_idname'):
                print(f"    - {attr_name} (bl_idname: {attr.bl_idname})")
    else:
        print("❌ Sous-module panels.outliner introuvable")
        
except ImportError as e:
    print(f"❌ Import panels échoué: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# =============== 3. VÉRIFICATION CLASSES ENREGISTRÉES ===============
print("\n🎯 ÉTAPE 3: Vérification classes Blender enregistrées")
print("-" * 80)

# Chercher tous les opérateurs QPanels Assets
qpanel_assets_operators = []
for op_name in dir(bpy.ops.qpanels_assets):
    if not op_name.startswith('_'):
        qpanel_assets_operators.append(op_name)

if qpanel_assets_operators:
    print(f"✅ {len(qpanel_assets_operators)} opérateur(s) enregistré(s):")
    for op_name in qpanel_assets_operators:
        op_full_name = f"bpy.ops.qpanels_assets.{op_name}()"
        print(f"  - {op_full_name}")
else:
    print("❌ Aucun opérateur qpanels_assets enregistré")
    print("   → Les classes n'ont pas été enregistrées via panels.register()")

# Vérifier spécifiquement l'opérateur Outliner
outliner_registered = hasattr(bpy.ops.qpanels_assets, 'outliner')
print(f"\nOutliner spécifique:")
print(f"  {'✅' if outliner_registered else '❌'} bpy.ops.qpanels_assets.outliner exists: {outliner_registered}")

# =============== 4. VÉRIFICATION TYPES BLENDER ===============
print("\n🔎 ÉTAPE 4: Recherche dans bpy.types")
print("-" * 80)

found_classes = []
for type_name in dir(bpy.types):
    if 'QPANEL_ASSET' in type_name:
        found_classes.append(type_name)

if found_classes:
    print(f"✅ {len(found_classes)} classe(s) QPanels Assets dans bpy.types:")
    for cls_name in found_classes:
        cls = getattr(bpy.types, cls_name)
        if hasattr(cls, 'bl_idname'):
            print(f"  - {cls_name} (bl_idname: {cls.bl_idname})")
        else:
            print(f"  - {cls_name}")
else:
    print("❌ Aucune classe QPANEL_ASSET trouvée dans bpy.types")
    print("   → panels.register() n'a probablement pas été appelé")

# =============== 5. TEST MANUEL IMPORT + REGISTER ===============
print("\n⚙️ ÉTAPE 5: Test manuel register")
print("-" * 80)

try:
    # Reload pour forcer re-import
    import importlib
    importlib.reload(panels)
    
    # Appeler register manuellement
    if hasattr(panels, 'register'):
        print("✅ Fonction panels.register() trouvée")
        print("   Appel de panels.register()...")
        panels.register()
        print("✅ panels.register() exécuté sans erreur")
        
        # Re-vérifier opérateurs
        qpanel_assets_operators_after = []
        for op_name in dir(bpy.ops.qpanels_assets):
            if not op_name.startswith('_'):
                qpanel_assets_operators_after.append(op_name)
        
        print(f"\n  Opérateurs après register: {len(qpanel_assets_operators_after)}")
        for op_name in qpanel_assets_operators_after:
            print(f"    - bpy.ops.qpanels_assets.{op_name}()")
    else:
        print("❌ Fonction panels.register() introuvable")
        print("   → panels/__init__.py ne définit pas register()")
        
except Exception as e:
    print(f"❌ Erreur lors du register: {e}")
    import traceback
    traceback.print_exc()

# =============== 6. VÉRIFICATION PANEL DANS SELECTOR ===============
print("\n🎨 ÉTAPE 6: Détection dans Panel Selector (QPanels)")
print("-" * 80)

# Chercher toutes les classes avec bl_qpanel_category
panel_candidates = []
for type_name in dir(bpy.types):
    try:
        cls = getattr(bpy.types, type_name)
        if hasattr(cls, 'bl_qpanel_category'):
            panel_candidates.append({
                'name': type_name,
                'category': cls.bl_qpanel_category,
                'bl_idname': getattr(cls, 'bl_idname', 'N/A')
            })
    except:
        pass

print(f"Panels avec bl_qpanel_category: {len(panel_candidates)}")
for panel in panel_candidates:
    marker = "🟢" if "QPANEL_ASSET" in panel['name'] else "⚪"
    print(f"  {marker} {panel['name']}")
    print(f"      Category: {panel['category']}")
    print(f"      bl_idname: {panel['bl_idname']}")

# =============== RÉSUMÉ FINAL ===============
print("\n" + "="*80)
print("📊 RÉSUMÉ DIAGNOSTIC")
print("="*80)

print(f"\n✅ Fichiers installés: {all_present}")
print(f"✅ Module panels importable: True")
print(f"{'✅' if qpanel_assets_operators else '❌'} Opérateurs enregistrés: {len(qpanel_assets_operators)}")
print(f"{'✅' if outliner_registered else '❌'} Outliner accessible: {outliner_registered}")
print(f"{'✅' if len(panel_candidates) > 0 else '❌'} Panels détectables: {len([p for p in panel_candidates if 'QPANEL_ASSET' in p['name']])}")

print("\n" + "="*80)
print("FIN DU DIAGNOSTIC")
print("="*80 + "\n")
