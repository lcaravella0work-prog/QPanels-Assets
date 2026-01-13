"""
QPanels Assets - Extension Package for QPanels
Provides additional panels for QPanels Core add-on

This is NOT a standalone Blender add-on.
It must be used with QPanels Core (v6.2.0+)
"""

bl_info = {
    "name": "QPanels Assets",
    "author": "QPanels Team",
    "version": (1, 0, 0),
    "blender": (3, 4, 0),
    "description": "Additional panels for QPanels",
    "category": "Interface",
}

# Import panels module for registration
from . import panels

def register():
    """Register all QPanels Assets panels"""
    panels.register()

def unregister():
    """Unregister all QPanels Assets panels"""
    panels.unregister()
