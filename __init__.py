# SPDX-License-Identifier: GPL-2.0-or-later

"""
QPanels Assets Package
Custom panels for QPanels addon system
"""

bl_info = {
    "name": "QPanels Assets",
    "author": "Ryan Inch (Collection Manager), Adapted by Soee",
    "version": (1, 0, 1),
    "blender": (3, 4, 0),
    "location": "Via QPanels Panel Selector",
    "description": "Custom UI panels for QPanels - Advanced Outliner and more",
    "warning": "Requires QPanels addon to function",
    "category": "Interface",
}

if "bpy" in locals():
    import importlib
    if "outliner" in locals():
        importlib.reload(outliner)
else:
    from . import outliner

import bpy


def get_custom_panels():
    """
    Return a dictionary of custom panels for QPanels.
    
    Returns:
        dict: Dictionary with panel_id as key and panel info as value
        Format: {
            "panel_id": {
                "module": module_reference,
                "operator": "operator.idname",
                "label": "Display Name",
                "icon": "ICON_NAME",
                "description": "Panel description"
            }
        }
    """
    return {
        "qpanel_outliner": {
            "module": outliner,
            "operator": "qpanel_outliner.open_outliner",
            "label": "QPanels Outliner",
            "icon": "OUTLINER",
            "description": "Advanced collection manager with restriction toggles and phantom mode"
        }
    }


def register():
    """Register all custom panels"""
    outliner.register()


def unregister():
    """Unregister all custom panels"""
    outliner.unregister()


if __name__ == "__main__":
    register()