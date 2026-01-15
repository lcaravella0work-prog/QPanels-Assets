"""
🔍 DIAGNOSTIC 2 - Test import module (SAFE - gère les erreurs)

UTILISATION:
1. Ouvrir Blender avec QPanels installé
2. Scripting > Text Editor > Open
3. Charger ce fichier
4. Run Script (Alt+P)
5. Lire résultats dans Console

NOTE: Ce script NE crash PAS Blender, il capture les erreurs proprement
"""

import sys
from pathlib import Path
import bpy

print("\n" + "="*80)
print("🔍 DIAGNOSTIC 2 - Test import module panels")
print("="*80 + "\n")

# Chemin Assets
scripts_addons = Path(bpy.utils.user_resource('SCRIPTS')) / "addons"
assets_dir = scripts_addons / "qpanel_assets"

print(f"📁 Assets dir: {assets_dir}")
print(f"   Existe: {assets_dir.exists()}\n")

if not assets_dir.exists():
    print("❌ qpanel_assets/ n'existe pas")
    sys.exit(1)

# Ajouter au sys.path
if str(assets_dir) not in sys.path:
    sys.path.insert(0, str(assets_dir))
    print(f"✅ Ajouté au sys.path\n")

# Test 1: Import du module panels
print("🔧 Test 1: Import panels")
try:
    import panels
    print("✅ Import panels réussi\n")
    
    # Lister attributs
    print("📦 Attributs de panels:")
    attrs = [a for a in dir(panels) if not a.startswith('_')]
    for attr in attrs:
        print(f"  - {attr}")
    
except ImportError as e:
    print(f"❌ Import panels échoué:")
    print(f"   {e}\n")
    
    # Afficher traceback complet
    import traceback
    print("📋 Traceback complet:")
    traceback.print_exc()
    print("\n⚠️ FIX: Vérifier les imports dans panels/__init__.py")

except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Import du sous-module outliner
print("\n🔧 Test 2: Import panels.outliner")
try:
    from panels import outliner
    print("✅ Import panels.outliner réussi\n")
    
    # Lister classes disponibles
    print("📦 Classes dans outliner:")
    for attr_name in dir(outliner):
        if attr_name.startswith('QPANEL_ASSET'):
            attr = getattr(outliner, attr_name)
            if hasattr(attr, '__name__'):
                print(f"  - {attr_name}")
    
except ImportError as e:
    print(f"❌ Import panels.outliner échoué:")
    print(f"   {e}\n")
    import traceback
    traceback.print_exc()

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("FIN DIAGNOSTIC 2")
print("="*80 + "\n")
