"""
QPanels Assets - Extension Package for QPanels Core

⚠️ NOT A STANDALONE BLENDER ADD-ON ⚠️

This package provides additional panels for QPanels and must be installed 
via QPanels Settings > Assets Tab (NOT via Blender Preferences > Add-ons).

Installation: QPanels Settings (F1) > License Tab > Assets Section > [Install]
Usage: Panel Selector (F2) > Category "QPanels Assets" > Select panel

Requires: QPanels Core v6.1.19+
Author: QPanels Team
Version: 2.1.3
"""

# bl_info intentionally removed to prevent QPanels Assets from appearing
# in Blender's Add-ons list (it's not a standalone add-on).
# Install and manage via QPanels Settings > Assets Tab only.

# Import panels module for registration
from . import panels

def register():
    """Register all QPanels Assets panels"""
    panels.register()

def unregister():
    """Unregister all QPanels Assets panels"""
    panels.unregister()
