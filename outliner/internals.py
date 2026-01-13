# SPDX-FileCopyrightText: 2011 Ryan Inch
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy

from bpy.types import (
    PropertyGroup,
    Operator,
)

from bpy.props import (
    StringProperty,
    IntProperty,
)

move_triggered = False
move_selection = []
move_active = None

layer_collections = {}
collection_tree = []
collection_state = {}
expanded = set()
row_index = 0
max_lvl = 0

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

expand_history = {
    "target": "",
    "history": [],
    }

phantom_history = {
    "view_layer": "",
    "initial_state": {},

    "exclude_history": {},
    "select_history": {},
    "hide_history": {},
    "disable_history": {},
    "render_history": {},
    "holdout_history": {},
    "indirect_history": {},

    "exclude_all_history": [],
    "select_all_history": [],
    "hide_all_history": [],
    "disable_all_history": [],
    "render_all_history": [],
    "holdout_all_history": [],
    "indirect_all_history": [],
                   }

copy_buffer = {
    "RTO": "",
    "values": []
    }

swap_buffer = {
    "A": {
        "RTO": "",
        "values": []
        },
    "B": {
        "RTO": "",
        "values": []
        }
    }


def update_col_name(self, context):
    global layer_collections
    global rto_history
    global expand_history

    if self.name != self.last_name:
        if self.name == '':
            self.name = self.last_name
            return

        # if statement prevents update on list creation
        if self.last_name != '':
            view_layer_name = context.view_layer.name

            # update collection name
            layer_collections[self.last_name]["ptr"].collection.name = self.name

            # update expanded
            orig_expanded = {x for x in expanded}

            if self.last_name in orig_expanded:
                expanded.remove(self.last_name)
                expanded.add(self.name)

            # update history
            rtos = [
                "exclude",
                "select",
                "hide",
                "disable",
                "render",
                "holdout",
                "indirect",
                ]

            orig_targets = {
                rto: rto_history[rto][view_layer_name]["target"]
                for rto in rtos
                if rto_history[rto].get(view_layer_name)
                }

            for rto in rtos:
                history = rto_history[rto].get(view_layer_name)

                if history and orig_targets[rto] == self.last_name:
                    history["target"] = self.name

            # update expand history
            orig_expand_target = expand_history["target"]
            orig_expand_history = [x for x in expand_history["history"]]

            if orig_expand_target == self.last_name:
                expand_history["target"] = self.name

            for x, name in enumerate(orig_expand_history):
                if name == self.last_name:
                    expand_history["history"][x] = self.name

            # update names in expanded and rto_history for any other
            # collection names that changed as a result of this name change
            qpo_list_collection = context.scene.qpanel_outliner.qpo_list_collection
            count = 0
            laycol_iter_list = list(context.view_layer.layer_collection.children)

            while laycol_iter_list:
                layer_collection = laycol_iter_list[0]
                qpo_list_item = qpo_list_collection[count]

                if qpo_list_item.name != layer_collection.name:
                    # update expanded
                    if qpo_list_item.last_name in orig_expanded:
                        if not qpo_list_item.last_name in layer_collections:
                            expanded.remove(qpo_list_item.name)

                        expanded.add(layer_collection.name)

                    # update history
                    for rto in rtos:
                        history = rto_history[rto].get(view_layer_name)

                        if history and orig_targets[rto] == qpo_list_item.last_name:
                            history["target"] = layer_collection.name

                    # update expand history
                    if orig_expand_target == qpo_list_item.last_name:
                        expand_history["target"] = layer_collection.name

                    for x, name in enumerate(orig_expand_history):
                        if name == qpo_list_item.last_name:
                            expand_history["history"][x] = layer_collection.name

                if layer_collection.children:
                    laycol_iter_list[0:0] = list(layer_collection.children)


                laycol_iter_list.remove(layer_collection)
                count += 1


            update_property_group(context)


        self.last_name = self.name


class QPOutlinerListCollection(PropertyGroup):
    name: StringProperty(update=update_col_name)
    last_name: StringProperty()


def update_collection_tree(context):
    global max_lvl
    global row_index
    global collection_tree
    global layer_collections

    collection_tree.clear()
    layer_collections.clear()

    max_lvl = 0
    row_index = 0
    layer_collection = context.view_layer.layer_collection
    init_laycol_list = layer_collection.children

    master_laycol = {"id": 0,
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

    get_all_collections(context, init_laycol_list, master_laycol, master_laycol["children"], visible=True)

    for laycol in master_laycol["children"]:
        collection_tree.append(laycol)


def get_all_collections(context, collections, parent, tree, level=0, visible=False):
    global row_index
    global max_lvl

    if level > max_lvl:
        max_lvl = level

    for item in collections:
        laycol = {"id": len(layer_collections) +1,
                  "name": item.name,
                  "lvl": level,
                  "row_index": row_index,
                  "visible":  visible,
                  "has_children": False,
                  "expanded": False,
                  "parent": parent,
                  "children": [],
                  "ptr": item
                  }

        row_index += 1

        layer_collections[item.name] = laycol
        tree.append(laycol)

        if len(item.children) > 0:
            laycol["has_children"] = True

            if item.name in expanded and laycol["visible"]:
                laycol["expanded"] = True
                get_all_collections(context, item.children, laycol, laycol["children"], level+1,  visible=True)

            else:
                get_all_collections(context, item.children, laycol, laycol["children"], level+1)


def update_property_group(context):
    global collection_tree

    update_collection_tree(context)
    context.scene.qpanel_outliner.qpo_list_collection.clear()
    create_property_group(context, collection_tree)


def create_property_group(context, tree):
    qpo = context.scene.qpanel_outliner

    for laycol in tree:
        new_qpo_listitem = qpo.qpo_list_collection.add()
        new_qpo_listitem.name = laycol["name"]

        if laycol["has_children"]:
            create_property_group(context, laycol["children"])


def get_modifiers(event):
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


def generate_state():
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


def check_state(context, *, qpo_popup=False, phantom_mode=False):
    view_layer = context.view_layer

    # check if expanded & history/buffer state still correct
    if qpo_popup and collection_state:
        new_state = generate_state()

        if new_state["name"] != collection_state["name"]:
            copy_buffer["RTO"] = ""
            copy_buffer["values"].clear()

            swap_buffer["A"]["RTO"] = ""
            swap_buffer["A"]["values"].clear()
            swap_buffer["B"]["RTO"] = ""
            swap_buffer["B"]["values"].clear()

            for name in list(expanded):
                laycol = layer_collections.get(name)
                if not laycol or not laycol["has_children"]:
                    expanded.remove(name)

            for name in list(expand_history["history"]):
                laycol = layer_collections.get(name)
                if not laycol or not laycol["has_children"]:
                    expand_history["history"].remove(name)

            for rto, history in rto_history.items():
                if view_layer.name in history:
                    del history[view_layer.name]


        else:
            for rto in ["exclude", "select", "hide", "disable", "render", "holdout", "indirect"]:
                if new_state[rto] != collection_state[rto]:
                    if view_layer.name in rto_history[rto]:
                        del rto_history[rto][view_layer.name]

                    if view_layer.name in rto_history[rto+"_all"]:
                        del rto_history[rto+"_all"][view_layer.name]


    if phantom_mode:
        qpo = context.scene.qpanel_outliner

        # check if in phantom mode and if it's still viable
        if qpo.in_phantom_mode:
            if layer_collections.keys() != phantom_history["initial_state"].keys():
                qpo.in_phantom_mode = False

            if view_layer.name != phantom_history["view_layer"]:
                qpo.in_phantom_mode = False

            if not qpo.in_phantom_mode:
                for key, value in phantom_history.items():
                    try:
                        value.clear()
                    except AttributeError:
                        if key == "view_layer":
                            phantom_history["view_layer"] = ""


def get_move_selection(*, names_only=False):
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
    global move_active
    global move_selection

    if not move_active:
        move_active = getattr(bpy.context.view_layer.objects.active, "name", None)

    if not always and move_active not in get_move_selection(names_only=True):
        move_active = None

    return bpy.data.objects[move_active] if move_active else None


class QPOutlinerSendReport(Operator):
    bl_label = "Send Report"
    bl_idname = "qpanel_outliner.send_report"

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
    def report():
        window = bpy.context.window_manager.windows[0]
        ctx = {'window': window, 'screen': window.screen, }
        bpy.ops.qpanel_outliner.send_report(ctx, 'INVOKE_DEFAULT', message=message)

    bpy.app.timers.register(report)


class QPOutlinerUISeparatorButton(Operator):
    bl_label = "UI Separator Button"
    bl_idname = "qpanel_outliner.ui_separator_button"

    def execute(self, context):
        return {'CANCELLED'}

def add_vertical_separator_line(row):
    # add buffer before to account for scaling
    separator = row.row()
    separator.scale_x = 0.1
    separator.label()

    # add separator line
    separator = row.row()
    separator.scale_x = 0.2
    separator.enabled = False
    separator.operator("qpanel_outliner.ui_separator_button",
                            text="",
                                icon='BLANK1',
                                )
    # add buffer after to account for scaling
    separator = row.row()
    separator.scale_x = 0.1
    separator.label()

def get_w_kwargs(func, **kwargs):
    def wrapper_func(self):
        return func(self, **kwargs)
    return wrapper_func

def get_transform_w_kwargs(func, **kwargs):
    def wrapper_func(self, curr_value, is_set):
        return func(self, curr_value, is_set, **kwargs)
    return wrapper_func

def set_w_kwargs(func, **kwargs):
    def wrapper_func(self, values):
        func(self, values, **kwargs)
    return wrapper_func

def set_transform_w_kwargs(func, **kwargs):
    def wrapper_func(self, new_value, curr_value, is_set):
        return func(self, new_value, curr_value, is_set, **kwargs)
    return wrapper_func
