"""
🔍 DIAGNOSTIC ULTRA-COMPLET - QPanels Assets (SAFE)

Ce script fait TOUS les tests en une seule exécution.
Exécuter APRÈS avoir cliqué [Install] dans QPanels Settings > Assets.

UTILISATION:
1. QPanels Settings (F1) > License Tab > Assets > [Install]
2. Attendre message "Installed successfully"
3. Scripting > Text Editor > Open ce fichier
4. Run Script (Alt+P)
5. Copier TOUTE la sortie console et l'envoyer
"""

import sys
import bpy
from pathlib import Path

print("\n" + "="*80)
print("🔍 DIAGNOSTIC ULTRA-COMPLET - QPANEL ASSETS v2.1.3")
print("="*80 + "\n")

# =============== CONFIG ===============
scripts_addons = Path(bpy.utils.user_resource('SCRIPTS')) / "addons"
assets_dir = scripts_addons / "qpanel_assets"
blender_version = f"{bpy.app.version[0]}.{bpy.app.version[1]}"

print(f"📍 Blender: {blender_version}")
print(f"📍 Scripts: {scripts_addons}")
print(f"📍 Assets:  {assets_dir}\n")

# =============== SECTION 1: FICHIERS ===============
print("="*80)
print("📁 SECTION 1: VÉRIFICATION FICHIERS")
print("="*80 + "\n")

if not assets_dir.exists():
    print("❌ ERREUR CRITIQUE: qpanel_assets/ n'existe PAS!")
    print("   → CAUSE: Installation n'a jamais été faite")
    print("   → SOLUTION: QPanels Settings > Assets > Cliquer [Install]")
    print("\n⚠️ ARRÊT DU DIAGNOSTIC - Pas de fichiers à analyser\n")
    sys.exit(1)

print(f"✅ Dossier qpanel_assets/ existe\n")

# Structure complète
print("📂 STRUCTURE COMPLÈTE:")
def show_tree(path, prefix="", max_depth=4, current_depth=0):
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        for i, item in enumerate(items):
            if item.name.startswith('__pycache__'):
                continue
            is_last = i == len(items) - 1
            marker = "└── " if is_last else "├── "
            size = f" ({item.stat().st_size} bytes)" if item.is_file() else ""
            print(f"{prefix}{marker}{item.name}{'/' if item.is_dir() else ''}{size}")
            
            if item.is_dir():
                extension = "    " if is_last else "│   "
                show_tree(item, prefix + extension, max_depth, current_depth + 1)
    except Exception as e:
        print(f"{prefix}  ⚠️ Erreur lecture: {e}")

show_tree(assets_dir)

# Fichiers critiques
print("\n✅ FICHIERS CRITIQUES:")
critical_files = {
    "version.json": assets_dir / "version.json",
    "__init__.py": assets_dir / "__init__.py",
    "panels/__init__.py": assets_dir / "panels" / "__init__.py",
    "panels/outliner/__init__.py": assets_dir / "panels" / "outliner" / "__init__.py",
    "panels/outliner/ui.py": assets_dir / "panels" / "outliner" / "ui.py",
    "panels/outliner/operators.py": assets_dir / "panels" / "outliner" / "operators.py",
    "panels/outliner/internals.py": assets_dir / "panels" / "outliner" / "internals.py",
}

all_files_ok = True
for name, path in critical_files.items():
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {name}")
    if not exists:
        all_files_ok = False
        print(f"       MANQUANT: {path}")

if not all_files_ok:
    print("\n❌ FICHIERS MANQUANTS - ZIP mal extrait!")
    print("   → Désinstaller et réinstaller Assets")
    sys.exit(1)

# Vérifier version.json
print("\n📄 CONTENU version.json:")
version_file = assets_dir / "version.json"
try:
    import json
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)
    print(f"  Version: {version_data.get('version', 'N/A')}")
    print(f"  SHA256:  {version_data.get('sha256', 'N/A')[:16]}...")
    print(f"  Size:    {version_data.get('size', 'N/A')} bytes")
except Exception as e:
    print(f"  ❌ Erreur lecture: {e}")

# Vérifier __init__.py (bl_info supprimé?)
print("\n📄 CONTENU __init__.py:")
init_file = assets_dir / "__init__.py"
try:
    with open(init_file, 'r', encoding='utf-8') as f:
        init_content = f.read()
    
    has_bl_info = 'bl_info' in init_content
    has_register = 'def register()' in init_content
    has_unregister = 'def unregister()' in init_content
    
    print(f"  bl_info présent: {'❌ OUI (devrait être supprimé!)' if has_bl_info else '✅ NON (correct)'}")
    print(f"  register() présent: {'✅' if has_register else '❌'}")
    print(f"  unregister() présent: {'✅' if has_unregister else '❌'}")
    
    if has_bl_info:
        print("\n  ⚠️ WARNING: bl_info encore présent!")
        print("     → Version pas à jour (devrait être v2.1.3 sans bl_info)")
except Exception as e:
    print(f"  ❌ Erreur lecture: {e}")

# =============== SECTION 2: IMPORTS ===============
print("\n" + "="*80)
print("📦 SECTION 2: TEST IMPORTS PYTHON")
print("="*80 + "\n")

# Ajouter au sys.path
if str(assets_dir) not in sys.path:
    sys.path.insert(0, str(assets_dir))
    print(f"✅ Ajouté au sys.path: {assets_dir}\n")
else:
    print(f"✅ Déjà dans sys.path\n")

# Test import panels
print("🔧 Test 1: import panels")
try:
    import panels
    print("✅ Import panels réussi\n")
    
    print("📋 Attributs de panels:")
    attrs = [a for a in dir(panels) if not a.startswith('_')]
    for attr in attrs:
        print(f"  - {attr}")
    
    has_register = hasattr(panels, 'register')
    has_unregister = hasattr(panels, 'unregister')
    print(f"\n  register() disponible: {'✅' if has_register else '❌'}")
    print(f"  unregister() disponible: {'✅' if has_unregister else '❌'}")
    
except ImportError as e:
    print(f"❌ Import panels ÉCHOUÉ:")
    print(f"   {e}\n")
    import traceback
    traceback.print_exc()
    print("\n⚠️ ARRÊT - Import impossible\n")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test import panels.outliner
print("\n🔧 Test 2: import panels.outliner")
try:
    from panels import outliner
    print("✅ Import panels.outliner réussi\n")
    
    print("📋 Classes QPANEL_ASSET dans outliner:")
    qpanel_classes = []
    for attr_name in dir(outliner):
        if attr_name.startswith('QPANEL_ASSET') or attr_name == 'CMListCollection' or attr_name == 'CollectionManagerProperties':
            qpanel_classes.append(attr_name)
            print(f"  - {attr_name}")
    
    print(f"\n  Total: {len(qpanel_classes)} classes trouvées")
    
    # Vérifier CMListCollection spécifiquement
    has_cmlist = hasattr(outliner, 'CMListCollection')
    has_cmprops = hasattr(outliner, 'CollectionManagerProperties')
    print(f"\n  CMListCollection exporté: {'✅' if has_cmlist else '❌ MANQUANT!'}")
    print(f"  CollectionManagerProperties exporté: {'✅' if has_cmprops else '❌'}")
    
    if not has_cmlist:
        print("\n  ⚠️ ERREUR: CMListCollection pas exporté!")
        print("     → Version pas à jour (devrait être v2.1.3)")
    
except ImportError as e:
    print(f"❌ Import panels.outliner ÉCHOUÉ:")
    print(f"   {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# =============== SECTION 3: REGISTRATION BLENDER ===============
print("\n" + "="*80)
print("🎯 SECTION 3: REGISTRATION BLENDER")
print("="*80 + "\n")

# Vérifier opérateurs
print("🔍 Opérateurs bpy.ops.qpanels_assets.*")
if hasattr(bpy.ops, 'qpanels_assets'):
    print("✅ Module bpy.ops.qpanels_assets existe\n")
    
    operators = [op for op in dir(bpy.ops.qpanels_assets) if not op.startswith('_')]
    if operators:
        print(f"📋 {len(operators)} opérateur(s) enregistré(s):")
        for op_name in operators:
            print(f"  - bpy.ops.qpanels_assets.{op_name}")
    else:
        print("❌ Aucun opérateur enregistré!")
        print("   → panels.register() n'a pas été appelé")
else:
    print("❌ Module bpy.ops.qpanels_assets N'EXISTE PAS")
    print("   → Assets pas chargé par QPanels Core")
    print("   → Vérifier assets_updater.py load_assets()")

# Vérifier classes bpy.types
print("\n🔍 Classes bpy.types.QPANEL_ASSET*")
qpanel_types = []
for type_name in dir(bpy.types):
    if 'QPANEL_ASSET' in type_name or type_name == 'CMListCollection' or type_name == 'CollectionManagerProperties':
        qpanel_types.append(type_name)

if qpanel_types:
    print(f"✅ {len(qpanel_types)} classe(s) dans bpy.types:\n")
    for cls_name in qpanel_types:
        try:
            cls = getattr(bpy.types, cls_name)
            bl_idname = getattr(cls, 'bl_idname', 'N/A')
            print(f"  - {cls_name}")
            if bl_idname != 'N/A':
                print(f"    bl_idname: {bl_idname}")
        except Exception as e:
            print(f"  - {cls_name} (erreur: {e})")
else:
    print("❌ AUCUNE classe QPANEL_ASSET dans bpy.types")
    print("   → panels.register() n'a JAMAIS été appelé")
    print("   → load_assets() a échoué")

# Vérifier WindowManager property
print("\n🔍 WindowManager.qpanel_assets_cm")
if hasattr(bpy.types.WindowManager, 'qpanel_assets_cm'):
    print("✅ Property qpanel_assets_cm enregistrée")
    
    # Tester accès
    try:
        cm = bpy.context.window_manager.qpanel_assets_cm
        print(f"   Accessible: ✅")
        print(f"   Type: {type(cm)}")
    except Exception as e:
        print(f"   ⚠️ Erreur accès: {e}")
else:
    print("❌ Property qpanel_assets_cm MANQUANTE")
    print("   → panels.register() n'a pas enregistré les properties")

# =============== SECTION 4: PANEL SELECTOR ===============
print("\n" + "="*80)
print("🎨 SECTION 4: DÉTECTION PANEL SELECTOR")
print("="*80 + "\n")

print("🔍 Recherche panels avec bl_qpanel_category")
panel_candidates = []
for type_name in dir(bpy.types):
    try:
        cls = getattr(bpy.types, type_name)
        if hasattr(cls, 'bl_qpanel_category'):
            panel_candidates.append({
                'name': type_name,
                'category': cls.bl_qpanel_category,
                'bl_idname': getattr(cls, 'bl_idname', 'N/A'),
                'bl_label': getattr(cls, 'bl_label', 'N/A')
            })
    except:
        pass

if panel_candidates:
    print(f"✅ {len(panel_candidates)} panel(s) détectable(s):\n")
    
    qpanel_assets_panels = []
    for panel in panel_candidates:
        marker = "🟢" if "QPANEL_ASSET" in panel['name'] else "⚪"
        print(f"{marker} {panel['name']}")
        print(f"   Category: {panel['category']}")
        print(f"   bl_idname: {panel['bl_idname']}")
        print(f"   bl_label: {panel['bl_label']}\n")
        
        if "QPANEL_ASSET" in panel['name']:
            qpanel_assets_panels.append(panel)
    
    print(f"🎯 QPanels Assets spécifiques: {len(qpanel_assets_panels)}")
    
    if len(qpanel_assets_panels) == 0:
        print("   ❌ AUCUN panel QPanels Assets détecté!")
        print("   → Devrait avoir au moins 'Outliner'")
else:
    print("❌ AUCUN panel détectable")
    print("   → bl_qpanel_category manquant ou mal défini")

# =============== SECTION 5: QPANELS CORE INTEGRATION ===============
print("\n" + "="*80)
print("🔌 SECTION 5: INTÉGRATION QPANELS CORE")
print("="*80 + "\n")

# Vérifier si QPanels Core charge Assets
print("🔍 Vérification qpanel.assets_updater")
try:
    from qpanel import assets_updater
    print("✅ Module assets_updater importé\n")
    
    # Vérifier si assets chargé
    has_assets_module = hasattr(assets_updater, '_assets_module')
    print(f"  _assets_module défini: {'✅' if has_assets_module else '❌'}")
    
    if has_assets_module:
        assets_mod = assets_updater._assets_module
        print(f"  Module: {assets_mod}")
    
    # Vérifier fonction load_assets
    has_load = hasattr(assets_updater, 'load_assets')
    print(f"  load_assets() disponible: {'✅' if has_load else '❌'}")
    
except ImportError as e:
    print(f"❌ Import assets_updater échoué: {e}")
except Exception as e:
    print(f"❌ Erreur: {e}")

# =============== RÉSUMÉ FINAL ===============
print("\n" + "="*80)
print("📊 RÉSUMÉ DIAGNOSTIC")
print("="*80 + "\n")

# Compteurs
files_ok = all_files_ok
import_ok = 'panels' in sys.modules
registered_ok = len(qpanel_types) > 0
panels_ok = len([p for p in panel_candidates if 'QPANEL_ASSET' in p['name']]) > 0

print("✅ CHECKLIST VALIDATION:\n")
print(f"  {'✅' if files_ok else '❌'} Fichiers installés correctement")
print(f"  {'✅' if import_ok else '❌'} Module panels importable")
print(f"  {'✅' if registered_ok else '❌'} Classes enregistrées dans Blender")
print(f"  {'✅' if panels_ok else '❌'} Panel(s) détectable(s) dans Panel Selector")

if files_ok and import_ok and registered_ok and panels_ok:
    print("\n🎉 TOUT FONCTIONNE!")
    print("   → Panel 'Outliner' devrait être visible dans Panel Selector (F2)")
    print("   → Catégorie: QPanels Assets")
elif not files_ok:
    print("\n❌ PROBLÈME: Fichiers manquants ou incomplets")
    print("   → SOLUTION: Désinstaller et réinstaller Assets")
elif not import_ok:
    print("\n❌ PROBLÈME: Import Python échoue")
    print("   → SOLUTION: Vérifier erreurs imports ci-dessus")
elif not registered_ok:
    print("\n❌ PROBLÈME: Classes pas enregistrées")
    print("   → SOLUTION: load_assets() n'a pas appelé panels.register()")
elif not panels_ok:
    print("\n❌ PROBLÈME: Aucun panel détectable")
    print("   → SOLUTION: bl_qpanel_category manquant ou incorrect")

print("\n" + "="*80)
print("FIN DIAGNOSTIC ULTRA-COMPLET")
print("="*80 + "\n")

print("📋 PROCHAINES ÉTAPES:")
print("   1. Copier TOUTE cette sortie console")
print("   2. L'envoyer au développeur")
print("   3. Inclure également la console Blender complète après installation")
print("\n")
