"""
🔍 DIAGNOSTIC 3 - Vérification opérateurs Blender (SAFE)

UTILISATION:
1. Ouvrir Blender avec QPanels installé ET Assets installé
2. Scripting > Text Editor > Open
3. Charger ce fichier
4. Run Script (Alt+P)
5. Lire résultats dans Console
"""

import bpy

print("\n" + "="*80)
print("🔍 DIAGNOSTIC 3 - Vérification opérateurs QPanels Assets")
print("="*80 + "\n")

# Chercher opérateurs qpanels_assets.*
print("🔍 Recherche opérateurs bpy.ops.qpanels_assets.*")

try:
    # Vérifier si le module existe
    if hasattr(bpy.ops, 'qpanels_assets'):
        print("✅ Module bpy.ops.qpanels_assets existe\n")
        
        # Lister tous les opérateurs
        operators = [op for op in dir(bpy.ops.qpanels_assets) if not op.startswith('_')]
        
        if operators:
            print(f"📋 {len(operators)} opérateur(s) trouvé(s):")
            for op_name in operators:
                # Tenter de récupérer l'opérateur
                try:
                    op = getattr(bpy.ops.qpanels_assets, op_name)
                    # Essayer d'obtenir description
                    bl_idname = f"qpanels_assets.{op_name}"
                    print(f"  ✅ {bl_idname}")
                except Exception as e:
                    print(f"  ⚠️ {op_name} (erreur: {e})")
        else:
            print("❌ Aucun opérateur trouvé")
            print("   → Assets pas chargé ou pas enregistré")
    else:
        print("❌ Module bpy.ops.qpanels_assets n'existe pas")
        print("   → Les Assets ne sont pas chargés")
        print("   → Vérifier dans QPanels Settings > Assets si installé")
        
except Exception as e:
    print(f"❌ Erreur lors de la recherche: {e}")
    import traceback
    traceback.print_exc()

# Chercher dans bpy.types
print("\n🔍 Recherche classes dans bpy.types")
found = []
for type_name in dir(bpy.types):
    if 'QPANEL_ASSET' in type_name:
        found.append(type_name)

if found:
    print(f"✅ {len(found)} classe(s) QPanels Assets dans bpy.types:")
    for cls_name in found:
        try:
            cls = getattr(bpy.types, cls_name)
            bl_idname = getattr(cls, 'bl_idname', 'N/A')
            print(f"  - {cls_name}")
            print(f"    bl_idname: {bl_idname}")
        except:
            print(f"  - {cls_name} (erreur lecture)")
else:
    print("❌ Aucune classe QPANEL_ASSET dans bpy.types")
    print("   → register() n'a pas été appelé")

# Vérifier WindowManager properties
print("\n🔍 Vérification WindowManager.qpanel_assets_cm")
if hasattr(bpy.types.WindowManager, 'qpanel_assets_cm'):
    print("✅ Property qpanel_assets_cm existe")
else:
    print("❌ Property qpanel_assets_cm manquante")
    print("   → panels.register() n'a pas enregistré les properties")

print("\n" + "="*80)
print("FIN DIAGNOSTIC 3")
print("="*80 + "\n")
