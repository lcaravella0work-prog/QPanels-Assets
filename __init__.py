# SPDX-License-Identifier: GPL-2.0-or-later

"""
QPanel Assets Package
Custom panels for QPanel addon system
"""

if "bpy" in locals():
    import importlib
    if "outliner" in locals():
        importlib.reload(outliner)
else:
    from . import outliner

import bpy


def get_custom_panels():
    """
    Return a dictionary of custom panels for QPanel.
    
    Returns:
        dict: Dictionary with panel_id as key and module as value
    """
    return {
        "qpanel_outliner": outliner
    }


def register():
    """Register all custom panels"""
    outliner.register()


def unregister():
    """Unregister all custom panels"""
    outliner.unregister()


if __name__ == "__main__":
    register()
