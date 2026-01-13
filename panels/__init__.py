"""
QPanels Assets - Panels Registration
Central registration point for all QPanels Assets panels
"""

import bpy

# Import all panel modules
from . import outliner

# List of all classes to register
classes = (
    # Outliner panel classes
    outliner.QPANEL_ASSET_OT_outliner,
    outliner.QPANEL_ASSET_OT_set_active_collection,
    outliner.QPANEL_ASSET_OT_expand_all_collections,
    outliner.QPANEL_ASSET_OT_expand_sublevel,
    outliner.QPANEL_ASSET_OT_select_collection_objects,
    outliner.QPANEL_ASSET_OT_rto_exclude_collection,
    outliner.QPANEL_ASSET_OT_rto_select_collection,
    outliner.QPANEL_ASSET_OT_rto_hide_collection,
    outliner.QPANEL_ASSET_OT_rto_disable_collection,
    outliner.QPANEL_ASSET_OT_rto_render_collection,
    outliner.QPANEL_ASSET_OT_rto_holdout_collection,
    outliner.QPANEL_ASSET_OT_rto_indirect_collection,
    outliner.QPANEL_ASSET_OT_remove_collection,
    outliner.QPANEL_ASSET_UL_collection_tree,
    outliner.CollectionManagerProperties,
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
