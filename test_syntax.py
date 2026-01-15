"""
Test de validation syntaxe Python (sans bpy)
Vérifie que tous les fichiers .py compilent correctement
"""

import sys
import py_compile
from pathlib import Path

panels_dir = Path(r"c:\Users\lcara\Documents\GitHub\QPanels-Core\QPanels-Assets\panels")

print("=" * 60)
print("QPANELS ASSETS v2.1.6 - VALIDATION SYNTAXE PYTHON")
print("=" * 60)

success_count = 0
fail_count = 0

for py_file in sorted(panels_dir.glob("*.py")):
    try:
        py_compile.compile(str(py_file), doraise=True)
        print(f"✅ {py_file.name:30s}")
        success_count += 1
    except py_compile.PyCompileError as e:
        print(f"❌ {py_file.name:30s} | {str(e.msg)[:60]}")
        fail_count += 1

print("=" * 60)
print(f"✅ SUCCESS: {success_count} fichiers")
print(f"❌ FAILED:  {fail_count} fichiers")
print("=" * 60)

if fail_count == 0:
    print("🎯 ALL SYNTAX VALIDATED - READY FOR BUILD")
    sys.exit(0)
else:
    print("⚠️ SYNTAX ERRORS FOUND - FIX REQUIRED")
    sys.exit(1)
