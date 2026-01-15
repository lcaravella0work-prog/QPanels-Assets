"""
QPanels Assets - Panels Registration
Central registration point for all QPanels Assets panels
"""

import bpy

# Import all panel modules
from . import outliner

# List of all classes to register
# IMPORTANT: PropertyGroups using CollectionProperty must be registered AFTER their referenced types
classes = (
    # PropertyGroups (register first)
    outliner.CMListCollection,  # Required by CollectionManagerProperties.cm_list_collection
    
    # Panel classes (for QPanels Panel Selector detection)
    outliner.QPANEL_ASSET_PT_outliner,  # Panel wrapper - enables QPanels detection
    
    # Outliner operator classes
    outliner.QPANEL_ASSET_OT_outliner,  # Operator implementation - standalone usage
    outliner.QPANEL_ASSET_OT_set_active_collection,
    outliner.QPANEL_ASSET_OT_expand_all,
    outliner.QPANEL_ASSET_OT_expand_sublevel,
    outliner.QPANEL_ASSET_OT_select_collection_objects,
    outliner.QPANEL_ASSET_OT_toggle_exclude,
    outliner.QPANEL_ASSET_OT_toggle_select,
    outliner.QPANEL_ASSET_OT_toggle_hide,
    outliner.QPANEL_ASSET_OT_toggle_disable,
    outliner.QPANEL_ASSET_OT_toggle_render,
    outliner.QPANEL_ASSET_OT_toggle_holdout,
    outliner.QPANEL_ASSET_OT_toggle_indirect,
    outliner.QPANEL_ASSET_OT_remove_collection,
    outliner.QPANEL_ASSET_UL_collection_tree,
    outliner.CollectionManagerProperties,  # MUST be after CMListCollection
)

def register():
    """Register all QPanels Assets panels"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register properties
    bpy.types.WindowManager.qpanel_assets_cm = bpy.props.PointerProperty(
        type=outliner.CollectionManagerProperties
    )
    
    print(f"[QPanels Assets] Registered {len(classes)} classes")

def unregister():
    """Unregister all QPanels Assets panels"""
    # Remove properties
    if hasattr(bpy.types.WindowManager, 'qpanel_assets_cm'):
        del bpy.types.WindowManager.qpanel_assets_cm
    
    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    print("[QPanels Assets] Unregistered all classes")
