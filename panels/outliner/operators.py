# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of QPanels Assets - Collection Outliner
# Original code from Collection Manager by Ryan Inch
# Adapted for QPanels Assets by QPanels Team

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, StringProperty, IntProperty

# Imports from internals
from . import internals
from .internals import (
    update_property_group,
    generate_state,
    check_state,
    get_modifiers,
    get_move_selection,
    get_move_active,
)

# Imports from operator_utils
from .operator_utils import (
    apply_to_children,
    isolate_rto,
    toggle_children,
    activate_all_rtos,
    invert_rtos,
    copy_rtos,
    swap_rtos,
    clear_copy,
    clear_swap,
    link_child_collections_to_parent,
    remove_collection,
    select_collection_objects,
    set_exclude_state,
    isolate_sel_objs_collections,
    disable_sel_objs_collections,
    get_rto,
    set_rto,
)


# =============== BASIC COLLECTION OPERATIONS ===============

class QPANEL_ASSET_OT_set_active_collection(Operator):
    """Set the active collection"""
    bl_label = "Set Active Collection"
    bl_idname = "qpanels_assets.outliner_set_active_collection"
    bl_options = {'UNDO'}

    is_master_collection: BoolProperty()
    collection_name: StringProperty()

    def execute(self, context):
        if self.is_master_collection:
            layer_collection = context.view_layer.layer_collection
        else:
            laycol = internals.layer_collections[self.collection_name]
            layer_collection = laycol["ptr"]

            # Set selection to this row
            cm = context.scene.collection_manager
            cm.cm_list_index = laycol["row_index"]

        context.view_layer.active_layer_collection = layer_collection

        if context.view_layer.active_layer_collection != layer_collection:
            self.report({'WARNING'}, "Can't set excluded collection as active")

        return {'FINISHED'}


class QPANEL_ASSET_OT_expand_all(Operator):
    """Expand/Collapse all collections"""
    bl_label = "Expand All Items"
    bl_idname = "qpanels_assets.outliner_expand_all"

    def execute(self, context):
        if len(internals.expanded) > 0:
            internals.expanded.clear()
            context.scene.collection_manager.cm_list_index = 0
        else:
            for laycol in internals.layer_collections.values():
                if laycol["ptr"].children:
                    internals.expanded.add(laycol["name"])

        # Clear expand history
        internals.expand_history["target"] = ""
        internals.expand_history["history"].clear()

        # Update tree view
        update_property_group(context)

        return {'FINISHED'}


class QPANEL_ASSET_OT_expand_sublevel(Operator):
    """Expand/Collapse sublevel collections"""
    bl_label = "Expand Sublevel Items"
    bl_description = (
        "  * Ctrl+LMB - Expand/Collapse all sublevels\n"
        "  * Shift+LMB - Isolate tree/Restore\n"
        "  * Alt+LMB - Discard history"
    )
    bl_idname = "qpanels_assets.outliner_expand_sublevel"

    expand: BoolProperty()
    name: StringProperty()
    index: IntProperty()

    def invoke(self, context, event):
        modifiers = get_modifiers(event)

        if modifiers == {"alt"}:
            internals.expand_history["target"] = ""
            internals.expand_history["history"].clear()

        elif modifiers == {"ctrl"}:
            # Expand/collapse all subcollections
            expand = None

            # Check whether to expand or collapse
            if self.name in internals.expanded:
                internals.expanded.remove(self.name)
                expand = False
            else:
                internals.expanded.add(self.name)
                expand = True

            # Do expanding/collapsing
            def set_expanded(layer_collection):
                if expand:
                    internals.expanded.add(layer_collection.name)
                else:
                    internals.expanded.discard(layer_collection.name)

            apply_to_children(internals.layer_collections[self.name]["ptr"], set_expanded)

            internals.expand_history["target"] = ""
            internals.expand_history["history"].clear()

        elif modifiers == {"shift"}:
            def isolate_tree(current_laycol):
                parent = current_laycol["parent"]

                for laycol in parent["children"]:
                    if (laycol["name"] != current_laycol["name"]
                    and laycol["name"] in internals.expanded):
                        internals.expanded.remove(laycol["name"])
                        internals.expand_history["history"].append(laycol["name"])

                if parent["parent"]:
                    isolate_tree(parent)

            if self.name == internals.expand_history["target"]:
                for item in internals.expand_history["history"]:
                    internals.expanded.add(item)

                internals.expand_history["target"] = ""
                internals.expand_history["history"].clear()

            else:
                internals.expand_history["target"] = ""
                internals.expand_history["history"].clear()

                isolate_tree(internals.layer_collections[self.name])
                internals.expand_history["target"] = self.name

        else:
            # Expand/collapse collection
            if self.expand:
                internals.expanded.add(self.name)
            else:
                internals.expanded.remove(self.name)

            internals.expand_history["target"] = ""
            internals.expand_history["history"].clear()

        # Set selected row to preserve scroll position
        context.scene.collection_manager.cm_list_index = self.index

        # Update tree view
        update_property_group(context)

        return {'FINISHED'}


class QPANEL_ASSET_OT_select_collection_objects(Operator):
    """Select objects in collection"""
    bl_label = "Select All Objects in the Collection"
    bl_description = (
        "  * LMB - Select all objects in collection\n"
        "  * Shift+LMB - Add/Remove collection objects from selection\n"
        "  * Ctrl+LMB - Isolate nested selection\n"
        "  * Ctrl+Shift+LMB - Add/Remove nested from selection"
    )
    bl_idname = "qpanels_assets.outliner_select_collection_objects"
    bl_options = {'REGISTER', 'UNDO'}

    is_master_collection: BoolProperty()
    collection_name: StringProperty()

    def invoke(self, context, event):
        modifiers = get_modifiers(event)

        if modifiers == {"shift"}:
            select_collection_objects(
                is_master_collection=self.is_master_collection,
                collection_name=self.collection_name,
                replace=False,
                nested=False
            )

        elif modifiers == {"ctrl"}:
            select_collection_objects(
                is_master_collection=self.is_master_collection,
                collection_name=self.collection_name,
                replace=True,
                nested=True
            )

        elif modifiers == {"ctrl", "shift"}:
            select_collection_objects(
                is_master_collection=self.is_master_collection,
                collection_name=self.collection_name,
                replace=False,
                nested=True
            )

        else:
            select_collection_objects(
                is_master_collection=self.is_master_collection,
                collection_name=self.collection_name,
                replace=True,
                nested=False
            )

        return {'FINISHED'}


# =============== RTO TOGGLE OPERATORS ===============

class CMRTOOperatorBase:
    """Base class for RTO toggle operators"""
    isolated = False

    def invoke(self, context, event):
        modifiers = get_modifiers(event)
        view_layer = context.view_layer.name

        if not view_layer in internals.rto_history[self.rto]:
            internals.rto_history[self.rto][view_layer] = {"target": "", "history": []}

        if not view_layer in internals.rto_history[self.rto+"_all"]:
            internals.rto_history[self.rto+"_all"][view_layer] = []

        if modifiers == {"alt"}:
            isolate_rto(self.__class__, self, view_layer, self.rto)

        elif modifiers == {"alt", "shift"}:
            isolate_rto(self.__class__, self, view_layer, self.rto, children=True)

        elif modifiers == {"ctrl"}:
            toggle_children(self, view_layer, self.rto)

        elif modifiers == {"shift"}:
            activate_all_rtos(view_layer, self.rto)

        elif modifiers == {"ctrl", "shift"}:
            invert_rtos(view_layer, self.rto)

        elif modifiers == {"ctrl", "alt"}:
            copy_rtos(view_layer, self.rto)

        elif modifiers == {"ctrl", "shift", "alt"}:
            swap_rtos(view_layer, self.rto)

        else:
            # Clear copy/swap buffers
            clear_copy(self.rto)
            clear_swap(self.rto)

            # Toggle RTO
            laycol_ptr = internals.layer_collections[self.name]["ptr"]
            state = not get_rto(laycol_ptr, self.rto)
            set_rto(laycol_ptr, self.rto, state)

            # Clear history
            del internals.rto_history[self.rto][view_layer]
            internals.rto_history[self.rto+"_all"].pop(view_layer, None)

        return {'FINISHED'}


class QPANEL_ASSET_OT_toggle_exclude(Operator, CMRTOOperatorBase):
    """Toggle exclude state"""
    bl_label = "Toggle Exclude"
    bl_description = (
        "  * LMB - Toggle exclude\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_exclude"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "exclude"


class QPANEL_ASSET_OT_toggle_select(Operator, CMRTOOperatorBase):
    """Toggle selectability"""
    bl_label = "Toggle Selectability"
    bl_description = (
        "  * LMB - Toggle selectability\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_select"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "select"


class QPANEL_ASSET_OT_toggle_hide(Operator, CMRTOOperatorBase):
    """Toggle viewport visibility"""
    bl_label = "Toggle Viewport Visibility"
    bl_description = (
        "  * LMB - Toggle viewport visibility\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_hide"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "hide"


class QPANEL_ASSET_OT_toggle_disable(Operator, CMRTOOperatorBase):
    """Toggle viewport disable"""
    bl_label = "Toggle Viewport Disable"
    bl_description = (
        "  * LMB - Toggle viewport disable\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_disable"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "disable"


class QPANEL_ASSET_OT_toggle_render(Operator, CMRTOOperatorBase):
    """Toggle render visibility"""
    bl_label = "Toggle Render Visibility"
    bl_description = (
        "  * LMB - Toggle render visibility\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_render"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "render"


class QPANEL_ASSET_OT_toggle_holdout(Operator, CMRTOOperatorBase):
    """Toggle holdout"""
    bl_label = "Toggle Holdout"
    bl_description = (
        "  * LMB - Toggle holdout\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_holdout"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "holdout"


class QPANEL_ASSET_OT_toggle_indirect(Operator, CMRTOOperatorBase):
    """Toggle indirect only"""
    bl_label = "Toggle Indirect Only"
    bl_description = (
        "  * LMB - Toggle indirect only\n"
        "  * Shift+LMB - Activate all/Restore\n"
        "  * Ctrl+LMB - Toggle children\n"
        "  * Alt+LMB - Isolate/Restore\n"
        "  * Alt+Shift+LMB - Isolate nested\n"
        "  * Ctrl+Shift+LMB - Invert\n"
        "  * Ctrl+Alt+LMB - Copy/Paste\n"
        "  * Ctrl+Shift+Alt+LMB - Swap"
    )
    bl_idname = "qpanels_assets.outliner_toggle_indirect"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()
    rto = "indirect"


# =============== COLLECTION MANAGEMENT OPERATORS ===============

class QPANEL_ASSET_OT_remove_collection(Operator):
    """Remove collection"""
    bl_label = "Remove Collection"
    bl_idname = "qpanels_assets.outliner_remove_collection"
    bl_options = {'UNDO'}

    collection_name: StringProperty()

    def execute(self, context):
        laycol = internals.layer_collections[self.collection_name]
        collection = laycol["ptr"].collection

        # Check if collection has children
        if len(collection.children) > 0:
            # Link children to parent
            parent_collection = laycol["parent"]["ptr"].collection
            link_child_collections_to_parent(laycol, collection, parent_collection)

        # Remove collection
        remove_collection(laycol, collection, context)

        return {'FINISHED'}


# =============== REGISTRATION ===============

classes = (
    QPANEL_ASSET_OT_set_active_collection,
    QPANEL_ASSET_OT_expand_all,
    QPANEL_ASSET_OT_expand_sublevel,
    QPANEL_ASSET_OT_select_collection_objects,
    QPANEL_ASSET_OT_toggle_exclude,
    QPANEL_ASSET_OT_toggle_select,
    QPANEL_ASSET_OT_toggle_hide,
    QPANEL_ASSET_OT_toggle_disable,
    QPANEL_ASSET_OT_toggle_render,
    QPANEL_ASSET_OT_toggle_holdout,
    QPANEL_ASSET_OT_toggle_indirect,
    QPANEL_ASSET_OT_remove_collection,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
