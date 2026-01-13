# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of QPanels Assets - Collection Outliner
# Original code from Collection Manager by Ryan Inch
# Adapted for QPanels Assets by QPanels Team

import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import StringProperty

# =============== GLOBAL STATE ===============

# {collection_name: laycol_dict}
layer_collections = {}

# List of top-level collection dicts
collection_tree = []

# Set of expanded collection names
expanded = set()

# RTO history for undo functionality
# {rto_name: {view_layer_name: [laycol_names]}}
rto_history = {
    "exclude": {},
    "exclude_all": {},
    "select": {},
    "select_all": {},
    "hide": {},
    "hide_all": {},
    "disable": {},
    "disable_all": {},
    "render": {},
    "render_all": {},
    "holdout": {},
    "holdout_all": {},
    "indirect": {},
    "indirect_all": {},
}

# Expansion history for undo
expand_history = {"target": "", "history": []}

# Buffer for copy/paste RTO values
copy_buffer = {"RTO": "", "values": []}
swap_buffer = {"A": {"RTO": "", "values": []}, "B": {"RTO": "", "values": []}}

# Current collection state for change detection
collection_state = {}

# Move operation tracking
move_selection = set()
move_active = None

# Tree building tracking
max_lvl = 0
row_index = 0

# Filter state
in_filter = False


# =============== PROPERTY GROUPS ===============

def update_col_name(self, context):
    """Update collection name when changed in UI."""
    if self.name != self.last_name:
        # Check if name already exists
        if self.name != self.last_name and self.name in layer_collections:
            # Restore previous name
            self.name = self.last_name
            return

        # Rename the actual collection
        laycol = layer_collections.get(self.last_name)
        if laycol:
            laycol["ptr"].collection.name = self.name
            
        self.last_name = self.name


class CMListCollection(PropertyGroup):
    """Property for each collection in the list."""
    name: StringProperty(update=update_col_name)
    last_name: StringProperty()


# =============== COLLECTION TREE BUILDING ===============

def update_collection_tree(context):
    """Rebuild the entire collection tree from current view layer."""
    global max_lvl, row_index, collection_tree, layer_collections

    collection_tree.clear()
    layer_collections.clear()

    max_lvl = 0
    row_index = 0
    layer_collection = context.view_layer.layer_collection
    init_laycol_list = layer_collection.children

    # Create master (root) collection dict
    master_laycol = {
        "id": 0,
        "name": layer_collection.name,
        "lvl": -1,
        "row_index": -1,
        "visible": True,
        "has_children": True,
        "expanded": True,
        "parent": None,
        "children": [],
        "ptr": layer_collection
    }

    # Recursively build tree
    get_all_collections(context, init_laycol_list, master_laycol, 
                       master_laycol["children"], visible=True)

    # Populate top-level tree
    for laycol in master_laycol["children"]:
        collection_tree.append(laycol)


def get_all_collections(context, collections, parent, tree, level=0, visible=False):
    """Recursively traverse layer collection hierarchy."""
    global row_index, max_lvl

    if level > max_lvl:
        max_lvl = level

    for item in collections:
        laycol = {
            "id": len(layer_collections) + 1,
            "name": item.name,
            "lvl": level,
            "row_index": row_index,
            "visible": visible,
            "has_children": False,
            "expanded": False,
            "parent": parent,
            "children": [],
            "ptr": item
        }

        row_index += 1

        layer_collections[item.name] = laycol
        tree.append(laycol)

        # Process children if they exist
        if len(item.children) > 0:
            laycol["has_children"] = True

            if item.name in expanded and laycol["visible"]:
                laycol["expanded"] = True
                get_all_collections(context, item.children, laycol, 
                                  laycol["children"], level+1, visible=True)
            else:
                get_all_collections(context, item.children, laycol, 
                                  laycol["children"], level+1)


def update_property_group(context):
    """Rebuild tree and update property group."""
    global collection_tree

    update_collection_tree(context)
    context.scene.collection_manager.cm_list_collection.clear()
    create_property_group(context, collection_tree)


def create_property_group(context, tree):
    """Create PropertyGroup items from collection tree."""
    cm = context.scene.collection_manager

    for laycol in tree:
        new_cm_listitem = cm.cm_list_collection.add()
        new_cm_listitem.name = laycol["name"]

        if laycol["has_children"]:
            create_property_group(context, laycol["children"])


# =============== STATE MANAGEMENT ===============

def generate_state():
    """Generate current state snapshot of all collections."""
    global layer_collections

    state = {
        "name": [],
        "exclude": [],
        "select": [],
        "hide": [],
        "disable": [],
        "render": [],
        "holdout": [],
        "indirect": [],
    }

    for name, laycol in layer_collections.items():
        state["name"].append(name)
        state["exclude"].append(laycol["ptr"].exclude)
        state["select"].append(laycol["ptr"].collection.hide_select)
        state["hide"].append(laycol["ptr"].hide_viewport)
        state["disable"].append(laycol["ptr"].collection.hide_viewport)
        state["render"].append(laycol["ptr"].collection.hide_render)
        state["holdout"].append(laycol["ptr"].holdout)
        state["indirect"].append(laycol["ptr"].indirect_only)

    return state


def check_state(context):
    """Check if collection state changed and invalidate history if needed."""
    view_layer = context.view_layer

    if collection_state:
        new_state = generate_state()

        # If collections were added/removed, clear buffers
        if new_state["name"] != collection_state["name"]:
            copy_buffer["RTO"] = ""
            copy_buffer["values"].clear()

            swap_buffer["A"]["RTO"] = ""
            swap_buffer["A"]["values"].clear()
            swap_buffer["B"]["RTO"] = ""
            swap_buffer["B"]["values"].clear()

            # Clean up expanded state
            for name in list(expanded):
                laycol = layer_collections.get(name)
                if not laycol or not laycol["has_children"]:
                    expanded.remove(name)

            # Clean up expand history
            for name in list(expand_history["history"]):
                laycol = layer_collections.get(name)
                if not laycol or not laycol["has_children"]:
                    expand_history["history"].remove(name)

            # Clear RTO history for this view layer
            for rto, history in rto_history.items():
                if view_layer.name in history:
                    del history[view_layer.name]

        else:
            # If RTO values changed externally, clear specific history
            for rto in ["exclude", "select", "hide", "disable", "render", "holdout", "indirect"]:
                if new_state[rto] != collection_state[rto]:
                    if view_layer.name in rto_history[rto]:
                        del rto_history[rto][view_layer.name]

                    if view_layer.name in rto_history[rto+"_all"]:
                        del rto_history[rto+"_all"][view_layer.name]


# =============== MOVE UTILITIES ===============

def get_move_selection(*, names_only=False):
    """Get objects selected for move operation."""
    global move_selection

    if not move_selection:
        move_selection = {obj.name for obj in bpy.context.selected_objects}

    if names_only:
        return move_selection
    else:
        if len(move_selection) <= 5:
            return {bpy.data.objects[name] for name in move_selection}
        else:
            return {obj for obj in bpy.data.objects if obj.name in move_selection}


def get_move_active(*, always=False):
    """Get active object for move operation."""
    global move_active, move_selection

    if not move_active:
        move_active = getattr(bpy.context.view_layer.objects.active, "name", None)

    if not always and move_active not in get_move_selection(names_only=True):
        move_active = None

    return bpy.data.objects[move_active] if move_active else None


# =============== EVENT UTILITIES ===============

def get_modifiers(event):
    """Extract modifier keys from event."""
    modifiers = []

    if event.alt:
        modifiers.append("alt")
    if event.ctrl:
        modifiers.append("ctrl")
    if event.oskey:
        modifiers.append("oskey")
    if event.shift:
        modifiers.append("shift")

    return set(modifiers)


# =============== UI UTILITIES ===============

class CMSendReport(Operator):
    """Display error/info messages in popup."""
    bl_label = "Send Report"
    bl_idname = "qpanels_assets.outliner_send_report"

    message: StringProperty()

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        first = True
        string = ""

        for num, char in enumerate(self.message):
            if char == "\n":
                if first:
                    col.row(align=True).label(text=string, icon='ERROR')
                    first = False
                else:
                    col.row(align=True).label(text=string, icon='BLANK1')

                string = ""
                continue

            string = string + char

        if first:
            col.row(align=True).label(text=string, icon='ERROR')
        else:
            col.row(align=True).label(text=string, icon='BLANK1')

    def invoke(self, context, event):
        wm = context.window_manager

        max_len = 0
        length = 0

        for char in self.message:
            if char == "\n":
                if length > max_len:
                    max_len = length
                length = 0
            else:
                length += 1

        if length > max_len:
            max_len = length

        return wm.invoke_popup(self, width=int(30 + (max_len*5.5)))

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}


def send_report(message):
    """Schedule error report to display."""
    def report():
        window = bpy.context.window_manager.windows[0]
        ctx = {'window': window, 'screen': window.screen}
        bpy.ops.qpanels_assets.outliner_send_report(ctx, 'INVOKE_DEFAULT', message=message)

    bpy.app.timers.register(report)


class CMUISeparatorButton(Operator):
    """Invisible operator for UI separator."""
    bl_label = "UI Separator Button"
    bl_idname = "qpanels_assets.outliner_ui_separator"

    def execute(self, context):
        return {'CANCELLED'}


def add_vertical_separator_line(row):
    """Add visual separator in UI row."""
    # Buffer before
    separator = row.row()
    separator.scale_x = 0.1
    separator.label()

    # Separator line
    separator = row.row()
    separator.scale_x = 0.2
    separator.enabled = False
    separator.operator("qpanels_assets.outliner_ui_separator",
                      text="", icon='BLANK1')

    # Buffer after
    separator = row.row()
    separator.scale_x = 0.1
    separator.label()


# =============== WRAPPER UTILITIES ===============

def get_w_kwargs(func, **kwargs):
    """Wrapper to inject kwargs into getter function."""
    def wrapper_func(self):
        return func(self, **kwargs)
    return wrapper_func


def get_transform_w_kwargs(func, **kwargs):
    """Wrapper to inject kwargs into transform getter."""
    def wrapper_func(self, curr_value, is_set):
        return func(self, curr_value, is_set, **kwargs)
    return wrapper_func


def set_w_kwargs(func, **kwargs):
    """Wrapper to inject kwargs into setter function."""
    def wrapper_func(self, values):
        func(self, values, **kwargs)
    return wrapper_func


def set_transform_w_kwargs(func, **kwargs):
    """Wrapper to inject kwargs into transform setter."""
    def wrapper_func(self, new_value, curr_value, is_set):
        return func(self, new_value, curr_value, is_set, **kwargs)
    return wrapper_func
