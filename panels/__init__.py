"""
QPanel Assets - Auto-Registration System
Automatically loads and registers all panel modules in this directory
"""

import bpy
import importlib
import sys
from pathlib import Path


# Modules list - will be populated dynamically
_modules = []
_registered = False


def discover_modules():
    """Auto-discover all Python modules in panels directory."""
    global _modules
    _modules.clear()
    
    panels_dir = Path(__file__).parent
    
    for py_file in panels_dir.glob("*.py"):
        # Skip __init__.py and private files
        if py_file.name.startswith("_"):
            continue
        
        module_name = py_file.stem
        full_module_name = f"{__package__}.{module_name}"
        
        try:
            # Import or reload module
            if full_module_name in sys.modules:
                module = importlib.reload(sys.modules[full_module_name])
            else:
                module = importlib.import_module(f".{module_name}", package=__package__)
            
            _modules.append(module)
        except Exception as e:
            print(f"[QPanel Assets] Failed to load {module_name}: {e}")


def register():
    """Register all discovered panel modules."""
    global _registered
    
    if _registered:
        return
    
    # Discover modules first
    discover_modules()
    
    # Register each module
    for module in _modules:
        if hasattr(module, 'register'):
            try:
                module.register()
            except Exception as e:
                print(f"[QPanel Assets] Failed to register {module.__name__}: {e}")
    
    _registered = True


def unregister():
    """Unregister all panel modules."""
    global _registered
    
    if not _registered:
        return
    
    for module in reversed(_modules):
        if hasattr(module, 'unregister'):
            try:
                module.unregister()
            except Exception as e:
                print(f"[QPanel Assets] Failed to unregister {module.__name__}: {e}")
    
    _modules.clear()
    _registered = False
