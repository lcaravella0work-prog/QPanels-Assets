# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of QPanels Assets - Collection Outliner
# Original code from Collection Manager by Ryan Inch
# Adapted for QPanels Assets by QPanels Team

import bpy
from bpy.types import Operator, UIList, PropertyGroup, Panel
from bpy.props import BoolProperty, StringProperty, IntProperty, CollectionProperty

# Imports from internals
from . import internals
from .internals import (
    update_collection_tree,
    update_property_group,
    get_move_selection,
    get_move_active,
)


# =============== MAIN OPERATOR (POPUP) ===============

class QPANEL_ASSET_OT_collection_outliner(Operator):
    """Manage collections in a popup UI"""
    bl_label = "Collection Outliner"
    bl_idname = "qpanels_assets.collection_outliner"
    
    # QPanels Assets marker
    bl_qpanel_category = "Outliner"

    last_view_layer = ""
    window_open = False

    master_collection: StringProperty(
        default='Scene Collection',
        name="",
        description="Scene Collection"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_open = True

    def draw(self, context):
        cls = QPANEL_ASSET_OT_collection_outliner
        layout = self.layout
        cm = context.scene.collection_manager
        view_layer = context.view_layer

        # Update tree if view layer changed
        if view_layer.name != cls.last_view_layer:
            update_collection_tree(context)
            cls.last_view_layer = view_layer.name

        # === HEADER ===
        header_row = layout.split(factor=0.5)
        main = header_row.row()
        view = header_row.row(align=True)
        view.alignment = 'RIGHT'

        main.label(text="Collection Outliner")

        # View layer selector
        view.prop(view_layer, "use", text="")
        view.separator()

        window = context.window
        scene = window.scene
        view.template_search(
            window, "view_layer",
            scene, "view_layers",
            new="scene.view_layer_add",
            unlink="scene.view_layer_remove"
        )

        layout.row().separator()

        # === EXPAND ALL BUTTON ===
        button_row = layout.row()
        button_row.alignment = 'LEFT'

        collapse_sec = button_row.row()
        collapse_sec.enabled = False

        if len(internals.expanded) > 0:
            text = "Collapse All Items"
        else:
            text = "Expand All Items"

        collapse_sec.operator("qpanels_assets.outliner_expand_all", text=text)

        # Enable button only if there are expandable collections
        for laycol in internals.collection_tree:
            if laycol["has_children"]:
                collapse_sec.enabled = True
                break

        layout.row().separator()

        # === MASTER COLLECTION ===
        mc_box = layout.box()
        master_row = mc_box.row(align=True)

        # Collection icon (active indicator)
        highlight = (context.view_layer.active_layer_collection ==
                    context.view_layer.layer_collection)

        prop = master_row.operator("qpanels_assets.outliner_set_active_collection",
                                   text='', icon='GROUP', depress=highlight)
        prop.is_master_collection = True
        prop.collection_name = 'Scene Collection'

        master_row.separator()

        # Collection name
        name_row = master_row.row(align=True)
        name_field = name_row.row(align=True)
        name_field.prop(self, "master_collection", text='')
        name_field.enabled = False

        # Select objects icon
        collection = context.view_layer.layer_collection.collection
        setsel = name_row.row(align=True)
        icon = 'BLANK1'
        some_selected = False

        if collection.objects:
            all_selected = all(obj.select_get() for obj in collection.objects 
                              if obj.visible_get() and not obj.hide_select)
            some_selected = any(obj.select_get() for obj in collection.objects)

            if all_selected:
                icon = 'KEYFRAME_HLT'
            elif some_selected:
                icon = 'KEYFRAME'
            else:
                icon = 'DOT'
        else:
            setsel.active = False

        prop = setsel.operator("qpanels_assets.outliner_select_collection_objects",
                              text="", icon=icon, depress=some_selected)
        prop.is_master_collection = True
        prop.collection_name = 'Scene Collection'

        # === COLLECTION LIST ===
        list_row = layout.row()
        list_row.template_list(
            "QPANEL_ASSET_UL_collection_tree",
            "",
            cm,
            "cm_list_collection",
            cm,
            "cm_list_index",
            rows=15,
            sort_lock=True
        )

        # Store selected objects for UIList
        selected_objects = get_move_selection()
        active_object = get_move_active()
        QPANEL_ASSET_UL_collection_tree.selected_objects = selected_objects
        QPANEL_ASSET_UL_collection_tree.active_object = active_object

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        # Initialize collection tree
        update_property_group(context)

        # Check state
        internals.collection_state.clear()
        internals.collection_state.update(internals.generate_state())

        # Show popup
        wm = context.window_manager
        return wm.invoke_popup(self, width=600)


# =============== UI LIST ===============

class QPANEL_ASSET_UL_collection_tree(UIList):
    """UIList for hierarchical collection tree"""
    
    selected_objects = set()
    active_object = None

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Get collection data
        laycol = internals.layer_collections.get(item.name)
        if not laycol:
            return

        # Don't draw if not visible in tree
        if not laycol["visible"]:
            return

        collection = laycol["ptr"].collection
        cm = context.scene.collection_manager

        # === INDENTATION ===
        row = layout.row(align=True)
        
        # Add indentation based on hierarchy level
        for _ in range(laycol["lvl"]):
            indent = row.row()
            indent.scale_x = 0.2
            indent.label(icon='BLANK1')

        # === EXPAND/COLLAPSE ===
        if laycol["has_children"]:
            if laycol["name"] in internals.expanded:
                icon = 'DISCLOSURE_TRI_DOWN'
                expand = False
            else:
                icon = 'DISCLOSURE_TRI_RIGHT'
                expand = True

            prop = row.operator("qpanels_assets.outliner_expand_sublevel",
                               text="", icon=icon, emboss=False)
            prop.expand = expand
            prop.name = item.name
            prop.index = index
        else:
            # Placeholder for alignment
            spacer = row.row()
            spacer.scale_x = 0.2
            spacer.label(icon='BLANK1')

        # === ACTIVE COLLECTION ICON ===
        highlight = (context.view_layer.active_layer_collection == laycol["ptr"])
        prop = row.operator("qpanels_assets.outliner_set_active_collection",
                           text='', icon='GROUP', depress=highlight, emboss=False)
        prop.is_master_collection = False
        prop.collection_name = item.name

        # === COLLECTION NAME ===
        name_row = row.row(align=True)
        name_row.prop(item, "name", text="", emboss=False, icon='OUTLINER_COLLECTION')

        # === SELECT OBJECTS ===
        setsel = row.row(align=True)
        icon = 'BLANK1'
        some_selected = False

        if collection.objects:
            all_selected = None
            
            for obj in collection.objects:
                if not obj.visible_get() or obj.hide_select:
                    continue
                    
                if not obj.select_get():
                    all_selected = False
                else:
                    some_selected = True
                    if all_selected == False:
                        break
                    all_selected = True

            if all_selected:
                icon = 'KEYFRAME_HLT'
            elif some_selected:
                icon = 'KEYFRAME'
            else:
                icon = 'DOT'
        else:
            setsel.active = False

        prop = setsel.operator("qpanels_assets.outliner_select_collection_objects",
                              text="", icon=icon, depress=some_selected, emboss=False)
        prop.is_master_collection = False
        prop.collection_name = item.name

        # === RTO TOGGLES ===
        rto_row = row.row(align=True)
        rto_row.alignment = 'RIGHT'

        # Exclude toggle
        if cm.show_exclude:
            icon = 'CHECKBOX_DEHLT' if laycol["ptr"].exclude else 'CHECKBOX_HLT'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_exclude",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Selectability toggle
        if cm.show_selectable:
            icon = 'RESTRICT_SELECT_ON' if collection.hide_select else 'RESTRICT_SELECT_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_select",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Hide viewport toggle
        if cm.show_hide_viewport:
            icon = 'HIDE_ON' if laycol["ptr"].hide_viewport else 'HIDE_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_hide",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Disable viewport toggle
        if cm.show_disable_viewport:
            icon = 'RESTRICT_VIEW_ON' if collection.hide_viewport else 'RESTRICT_VIEW_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_disable",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Render toggle
        if cm.show_render:
            icon = 'RESTRICT_RENDER_ON' if collection.hide_render else 'RESTRICT_RENDER_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_render",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Holdout toggle
        if cm.show_holdout:
            icon = 'HOLDOUT_ON' if laycol["ptr"].holdout else 'HOLDOUT_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_holdout",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name

        # Indirect toggle
        if cm.show_indirect:
            icon = 'INDIRECT_ONLY_ON' if laycol["ptr"].indirect_only else 'INDIRECT_ONLY_OFF'
            prop = rto_row.operator("qpanels_assets.outliner_toggle_indirect",
                                   text="", icon=icon, emboss=False)
            prop.name = item.name


# =============== PROPERTY GROUP ===============

class CollectionManagerProperties(PropertyGroup):
    """Properties for Collection Manager"""
    
    cm_list_collection: CollectionProperty(type=internals.CMListCollection)
    cm_list_index: IntProperty()
    
    # RTO visibility toggles
    show_exclude: BoolProperty(default=True, name="Exclude")
    show_selectable: BoolProperty(default=True, name="Selectability")
    show_hide_viewport: BoolProperty(default=True, name="Hide Viewport")
    show_disable_viewport: BoolProperty(default=True, name="Disable Viewport")
    show_render: BoolProperty(default=True, name="Render")
    show_holdout: BoolProperty(default=False, name="Holdout")
    show_indirect: BoolProperty(default=False, name="Indirect Only")


# =============== REGISTRATION ===============

classes = (
    CollectionManagerProperties,
    QPANEL_ASSET_OT_collection_outliner,
    QPANEL_ASSET_UL_collection_tree,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register property group
    bpy.types.Scene.collection_manager = bpy.props.PointerProperty(
        type=CollectionManagerProperties
    )


def unregister():
    # Unregister property group
    del bpy.types.Scene.collection_manager
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
