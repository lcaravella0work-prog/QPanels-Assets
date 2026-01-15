"""
Test d'import de tous les panels v5.4.0
Validation avant build final
"""

import sys
from pathlib import Path

# Add panels directory to path
panels_dir = Path(__file__).parent / "panels"
sys.path.insert(0, str(panels_dir.parent))

panels_list = [
    "properties",
    "properties_data_armature",
    "properties_data_camera",
    "properties_data_curve",
    "properties_data_light",
    "properties_data_mesh",
    "properties_particle",
    "properties_physics",
    "properties_render",
    "properties_scene",
    "properties_texture",
    "space_dopesheet",
    "space_graph",
    "space_image",
    "space_nla",
    "space_node",
    "space_sequencer",
    "view3d",
    "outliner"
]

success_count = 0
fail_count = 0

print("=" * 60)
print("QPANELS ASSETS v2.1.6 - TEST D'IMPORTS")
print("=" * 60)

for panel_name in panels_list:
    try:
        module = __import__(f"panels.{panel_name}", fromlist=[''])
        
        # Check for register/unregister functions
        has_register = hasattr(module, 'register')
        has_unregister = hasattr(module, 'unregister')
        
        status = "✅"
        if not (has_register and has_unregister):
            status = "⚠️"
            
        print(f"{status} {panel_name:30s} | register: {has_register} | unregister: {has_unregister}")
        success_count += 1
        
    except Exception as e:
        print(f"❌ {panel_name:30s} | ERROR: {str(e)[:60]}")
        fail_count += 1

print("=" * 60)
print(f"✅ SUCCESS: {success_count}/{len(panels_list)}")
print(f"❌ FAILED:  {fail_count}/{len(panels_list)}")
print("=" * 60)

if fail_count == 0:
    print("🎯 ALL IMPORTS VALIDATED - READY FOR BUILD")
else:
    print("⚠️ SOME IMPORTS FAILED - FIX REQUIRED")
