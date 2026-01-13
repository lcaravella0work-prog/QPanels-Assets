# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of QPanels Assets - Collection Outliner
# Original code from Collection Manager by Ryan Inch
# Adapted for QPanels Assets by QPanels Team

import bpy

# Import from internals
from . import internals
from .internals import (
    update_property_group,
    get_move_selection,
    get_move_active,
)

# =============== MODE CONVERTER ===============

mode_converter = {
    'EDIT_MESH': 'EDIT',
    'EDIT_CURVE': 'EDIT',
    'EDIT_SURFACE': 'EDIT',
    'EDIT_TEXT': 'EDIT',
    'EDIT_ARMATURE': 'EDIT',
    'EDIT_METABALL': 'EDIT',
    'EDIT_LATTICE': 'EDIT',
    'POSE': 'POSE',
    'SCULPT': 'SCULPT',
    'PAINT_WEIGHT': 'WEIGHT_PAINT',
    'PAINT_VERTEX': 'VERTEX_PAINT',
    'PAINT_TEXTURE': 'TEXTURE_PAINT',
    'PARTICLE': 'PARTICLE_EDIT',
    'OBJECT': 'OBJECT',
    'PAINT_GPENCIL': 'PAINT_GPENCIL',
    'EDIT_GPENCIL': 'EDIT_GPENCIL',
    'SCULPT_GPENCIL': 'SCULPT_GPENCIL',
    'WEIGHT_GPENCIL': 'WEIGHT_GPENCIL',
    'VERTEX_GPENCIL': 'VERTEX_GPENCIL',
}

# =============== RTO CONFIGURATION ===============

rto_path = {
    "exclude": "exclude",
    "select": "collection.hide_select",
    "hide": "hide_viewport",
    "disable": "collection.hide_viewport",
    "render": "collection.hide_render",
    "holdout": "holdout",
    "indirect": "indirect_only",
}

set_off_on = {
    "exclude": {"off": True, "on": False},
    "select": {"off": True, "on": False},
    "hide": {"off": True, "on": False},
    "disable": {"off": True, "on": False},
    "render": {"off": True, "on": False},
    "holdout": {"off": False, "on": True},
    "indirect": {"off": False, "on": True}
}

get_off_on = {
    False: {
        "exclude": "on",
        "select": "on",
        "hide": "on",
        "disable": "on",
        "render": "on",
        "holdout": "off",
        "indirect": "off",
    },
    True: {
        "exclude": "off",
        "select": "off",
        "hide": "off",
        "disable": "off",
        "render": "off",
        "holdout": "on",
        "indirect": "on",
    }
}


# =============== RTO GETTERS/SETTERS ===============

def get_rto(layer_collection, rto):
    """Get RTO state from layer collection."""
    if rto in ["exclude", "hide", "holdout", "indirect"]:
        return getattr(layer_collection, rto_path[rto])
    else:
        collection = getattr(layer_collection, "collection")
        return getattr(collection, rto_path[rto].split(".")[1])


def set_rto(layer_collection, rto, value):
    """Set RTO state on layer collection."""
    if rto in ["exclude", "hide", "holdout", "indirect"]:
        setattr(layer_collection, rto_path[rto], value)
    else:
        collection = getattr(layer_collection, "collection")
        setattr(collection, rto_path[rto].split(".")[1], value)


# =============== RECURSIVE UTILITIES ===============

def apply_to_children(parent, apply_function, *args, **kwargs):
    """Recursively apply a function to all children collections."""
    child_lists = [parent.children]

    while child_lists:
        new_child_lists = []

        for child_list in child_lists:
            for child in child_list:
                apply_function(child, *args, **kwargs)

                if child.children:
                    new_child_lists.append(child.children)

        child_lists = new_child_lists


# =============== ISOLATION OPERATIONS ===============

def isolate_rto(cls, self, view_layer, rto, *, children=False):
    """Isolate a collection's RTO, or restore previous state."""
    off = set_off_on[rto]["off"]
    on = set_off_on[rto]["on"]

    laycol_ptr = internals.layer_collections[self.name]["ptr"]
    target = internals.rto_history[rto][view_layer].get("target")
    history = internals.rto_history[rto][view_layer].get("history", [])

    # Get active collections
    active_layer_collections = [x["ptr"] for x in internals.layer_collections.values()
                                if get_rto(x["ptr"], rto) == on]

    # Check if previous state should be restored
    if cls.isolated and self.name == target:
        # Restore previous state
        for x, item in enumerate(internals.layer_collections.values()):
            set_rto(item["ptr"], rto, history[x])

        # Reset target and history
        del internals.rto_history[rto][view_layer]
        cls.isolated = False

    # Check if all RTOs should be activated
    elif (len(active_layer_collections) == 1 and
          active_layer_collections[0].name == self.name):
        # Activate all collections
        for item in internals.layer_collections.values():
            set_rto(item["ptr"], rto, on)

        # Reset target and history
        internals.rto_history[rto].pop(view_layer, None)
        cls.isolated = False

    else:
        # Isolate collection
        internals.rto_history[rto][view_layer] = {"target": self.name, "history": []}
        history = internals.rto_history[rto][view_layer]["history"]

        # Save state
        for item in internals.layer_collections.values():
            history.append(get_rto(item["ptr"], rto))

        child_states = {}
        if children:
            # Get child states
            def get_child_states(layer_collection):
                child_states[layer_collection.name] = get_rto(layer_collection, rto)

            apply_to_children(laycol_ptr, get_child_states)

        # Isolate collection
        for item in internals.layer_collections.values():
            if item["name"] != laycol_ptr.name:
                set_rto(item["ptr"], rto, off)

        set_rto(laycol_ptr, rto, on)

        if rto not in ["exclude", "holdout", "indirect"]:
            # Activate all parents
            laycol = internals.layer_collections[self.name]
            while laycol["id"] != 0:
                set_rto(laycol["ptr"], rto, on)
                laycol = laycol["parent"]

            if children:
                # Restore child states
                def restore_child_states(layer_collection):
                    set_rto(layer_collection, rto, child_states[layer_collection.name])

                apply_to_children(laycol_ptr, restore_child_states)

        else:
            if children:
                # Restore child states
                def restore_child_states(layer_collection):
                    set_rto(layer_collection, rto, child_states[layer_collection.name])

                apply_to_children(laycol_ptr, restore_child_states)

            elif rto == "exclude":
                # Deactivate all children
                def deactivate_all_children(layer_collection):
                    set_rto(layer_collection, rto, True)

                apply_to_children(laycol_ptr, deactivate_all_children)

        cls.isolated = True


def isolate_sel_objs_collections(view_layer, rto, *, use_active=False):
    """Isolate collections containing selected objects."""
    selected_objects = get_move_selection()

    if use_active:
        selected_objects.add(get_move_active(always=True))

    if not selected_objects:
        return "No selected objects"

    off = set_off_on[rto]["off"]
    on = set_off_on[rto]["on"]

    history = internals.rto_history[rto+"_all"][view_layer]

    # If not isolated, isolate collections of selected objects
    if len(history) == 0:
        keep_history = False

        # Save history and isolate RTOs
        for item in internals.layer_collections.values():
            history.append(get_rto(item["ptr"], rto))
            rto_state = off

            # Check if any selected objects are in the collection
            if not set(selected_objects).isdisjoint(item["ptr"].collection.objects):
                rto_state = on

            if history[-1] != rto_state:
                keep_history = True

            if rto == "exclude":
                set_exclude_state(item["ptr"], rto_state)
            else:
                set_rto(item["ptr"], rto, rto_state)

                # Activate all parents if needed
                if rto_state == on and rto not in ["holdout", "indirect"]:
                    laycol = item["parent"]
                    while laycol["id"] != 0:
                        set_rto(laycol["ptr"], rto, on)
                        laycol = laycol["parent"]

        if not keep_history:
            history.clear()
            return "Collection already isolated"

    else:
        # Restore state
        for x, item in enumerate(internals.layer_collections.values()):
            set_rto(item["ptr"], rto, history[x])

        # Clear history
        del internals.rto_history[rto+"_all"][view_layer]


def disable_sel_objs_collections(view_layer, rto):
    """Disable RTOs for collections containing selected objects."""
    off = set_off_on[rto]["off"]
    selected_objects = get_move_selection()

    history = internals.rto_history[rto+"_all"][view_layer]

    if not selected_objects and not history:
        del internals.rto_history[rto+"_all"][view_layer]
        return "No selected objects"

    # If not disabled, disable collections of selected objects
    if len(history) == 0:
        # Save history and disable RTOs
        for item in internals.layer_collections.values():
            history.append(get_rto(item["ptr"], rto))

            # Check if any selected objects are in the collection
            if not set(selected_objects).isdisjoint(item["ptr"].collection.objects):
                if rto == "exclude":
                    set_exclude_state(item["ptr"], off)
                else:
                    set_rto(item["ptr"], rto, off)

    else:
        # Restore state
        for x, item in enumerate(internals.layer_collections.values()):
            set_rto(item["ptr"], rto, history[x])

        # Clear history
        del internals.rto_history[rto+"_all"][view_layer]


# =============== TOGGLE OPERATIONS ===============

def toggle_children(self, view_layer, rto):
    """Toggle RTO state for collection and all children."""
    laycol_ptr = internals.layer_collections[self.name]["ptr"]
    
    # Clear RTO history
    internals.rto_history[rto].pop(view_layer, None)
    internals.rto_history[rto+"_all"].pop(view_layer, None)

    # Toggle RTO state
    state = not get_rto(laycol_ptr, rto)
    set_rto(laycol_ptr, rto, state)

    def set_state(layer_collection):
        set_rto(layer_collection, rto, state)

    apply_to_children(laycol_ptr, set_state)


def activate_all_rtos(view_layer, rto):
    """Activate RTO for all collections, or restore previous state."""
    off = set_off_on[rto]["off"]
    on = set_off_on[rto]["on"]

    history = internals.rto_history[rto+"_all"][view_layer]

    # If not activated, activate all
    if len(history) == 0:
        keep_history = False

        for item in reversed(list(internals.layer_collections.values())):
            if get_rto(item["ptr"], rto) == off:
                keep_history = True

            history.append(get_rto(item["ptr"], rto))
            set_rto(item["ptr"], rto, on)

        if not keep_history:
            history.clear()

        history.reverse()

    else:
        # Restore state
        for x, item in enumerate(internals.layer_collections.values()):
            set_rto(item["ptr"], rto, history[x])

        # Clear RTO history
        del internals.rto_history[rto+"_all"][view_layer]


def invert_rtos(view_layer, rto):
    """Invert RTO state for all collections."""
    if rto == "exclude":
        orig_values = []

        for item in internals.layer_collections.values():
            orig_values.append(get_rto(item["ptr"], rto))

        for x, item in enumerate(internals.layer_collections.values()):
            set_rto(item["ptr"], rto, not orig_values[x])

    else:
        for item in internals.layer_collections.values():
            set_rto(item["ptr"], rto, not get_rto(item["ptr"], rto))

    # Clear RTO history
    internals.rto_history[rto].pop(view_layer, None)


# =============== COPY/PASTE OPERATIONS ===============

def copy_rtos(view_layer, rto):
    """Copy RTO state, or paste if already copied."""
    if not internals.copy_buffer["RTO"]:
        # Copy
        internals.copy_buffer["RTO"] = rto
        for laycol in internals.layer_collections.values():
            internals.copy_buffer["values"].append(
                get_off_on[get_rto(laycol["ptr"], rto)][rto]
            )

    else:
        # Paste
        for x, laycol in enumerate(internals.layer_collections.values()):
            set_rto(laycol["ptr"], rto,
                   set_off_on[rto][internals.copy_buffer["values"][x]])

        # Clear RTO history
        internals.rto_history[rto].pop(view_layer, None)
        internals.rto_history[rto+"_all"].pop(view_layer, None)

        # Clear copy buffer
        internals.copy_buffer["RTO"] = ""
        internals.copy_buffer["values"].clear()


def swap_rtos(view_layer, rto):
    """Swap two RTO states."""
    if not internals.swap_buffer["A"]["values"]:
        # Get A
        internals.swap_buffer["A"]["RTO"] = rto
        for laycol in internals.layer_collections.values():
            internals.swap_buffer["A"]["values"].append(
                get_off_on[get_rto(laycol["ptr"], rto)][rto]
            )

    else:
        # Get B
        internals.swap_buffer["B"]["RTO"] = rto
        for laycol in internals.layer_collections.values():
            internals.swap_buffer["B"]["values"].append(
                get_off_on[get_rto(laycol["ptr"], rto)][rto]
            )

        # Swap A with B
        for x, laycol in enumerate(internals.layer_collections.values()):
            set_rto(laycol["ptr"], internals.swap_buffer["A"]["RTO"],
                   set_off_on[internals.swap_buffer["A"]["RTO"]][
                       internals.swap_buffer["B"]["values"][x]])

            set_rto(laycol["ptr"], internals.swap_buffer["B"]["RTO"],
                   set_off_on[internals.swap_buffer["B"]["RTO"]][
                       internals.swap_buffer["A"]["values"][x]])

        # Clear RTO history
        swap_a = internals.swap_buffer["A"]["RTO"]
        swap_b = internals.swap_buffer["B"]["RTO"]

        internals.rto_history[swap_a].pop(view_layer, None)
        internals.rto_history[swap_a+"_all"].pop(view_layer, None)
        internals.rto_history[swap_b].pop(view_layer, None)
        internals.rto_history[swap_b+"_all"].pop(view_layer, None)

        # Clear swap buffer
        internals.swap_buffer["A"]["RTO"] = ""
        internals.swap_buffer["A"]["values"].clear()
        internals.swap_buffer["B"]["RTO"] = ""
        internals.swap_buffer["B"]["values"].clear()


def clear_copy(rto):
    """Clear copy buffer if it matches the RTO."""
    if internals.copy_buffer["RTO"] == rto:
        internals.copy_buffer["RTO"] = ""
        internals.copy_buffer["values"].clear()


def clear_swap(rto):
    """Clear swap buffer if it matches the RTO."""
    if internals.swap_buffer["A"]["RTO"] == rto:
        internals.swap_buffer["A"]["RTO"] = ""
        internals.swap_buffer["A"]["values"].clear()
        internals.swap_buffer["B"]["RTO"] = ""
        internals.swap_buffer["B"]["values"].clear()


# =============== COLLECTION MANAGEMENT ===============

def link_child_collections_to_parent(laycol, collection, parent_collection):
    """Link child collections to parent before deletion."""
    # Store view layer RTOs for all children
    child_states = {}
    
    def get_child_states(layer_collection):
        child_states[layer_collection.name] = (
            layer_collection.exclude,
            layer_collection.hide_viewport,
            layer_collection.holdout,
            layer_collection.indirect_only
        )

    apply_to_children(laycol["ptr"], get_child_states)

    # Link subcollections to parent
    for subcollection in collection.children:
        if subcollection.name not in parent_collection.children:
            parent_collection.children.link(subcollection)

    # Restore view layer RTOs
    def restore_child_states(layer_collection):
        state = child_states.get(layer_collection.name)
        if state:
            layer_collection.exclude = state[0]
            layer_collection.hide_viewport = state[1]
            layer_collection.holdout = state[2]
            layer_collection.indirect_only = state[3]

    apply_to_children(laycol["parent"]["ptr"], restore_child_states)


def remove_collection(laycol, collection, context):
    """Remove collection and update references."""
    # Get selected row
    cm = context.scene.collection_manager
    selected_row_name = cm.cm_list_collection[cm.cm_list_index].name

    # Delete collection
    bpy.data.collections.remove(collection)

    # Update references
    internals.expanded.discard(laycol["name"])

    if internals.expand_history["target"] == laycol["name"]:
        internals.expand_history["target"] = ""

    if laycol["name"] in internals.expand_history["history"]:
        internals.expand_history["history"].remove(laycol["name"])

    # Reset history
    for rto in internals.rto_history.values():
        rto.clear()

    # Update tree view
    update_property_group(context)

    # Update selected row
    laycol = internals.layer_collections.get(selected_row_name, None)
    if laycol:
        cm.cm_list_index = laycol["row_index"]
    elif len(cm.cm_list_collection) <= cm.cm_list_index:
        cm.cm_list_index = len(cm.cm_list_collection) - 1

        if cm.cm_list_index > -1:
            name = cm.cm_list_collection[cm.cm_list_index].name
            laycol = internals.layer_collections[name]
            while not laycol["visible"]:
                laycol = laycol["parent"]

            cm.cm_list_index = laycol["row_index"]


def select_collection_objects(is_master_collection, collection_name, replace, nested, selection_state=None):
    """Select objects in a collection."""
    if bpy.context.mode != 'OBJECT':
        return

    if is_master_collection:
        target_collection = bpy.context.view_layer.layer_collection.collection
    else:
        laycol = internals.layer_collections[collection_name]
        target_collection = laycol["ptr"].collection

    if replace:
        bpy.ops.object.select_all(action='DESELECT')

    if selection_state is None:
        selection_state = get_move_selection().isdisjoint(target_collection.objects)

    def select_objects(collection, selection_state):
        for obj in collection.objects:
            try:
                obj.select_set(selection_state)
            except RuntimeError:
                pass

    select_objects(target_collection, selection_state)

    if nested:
        apply_to_children(target_collection, select_objects, selection_state)


def set_exclude_state(target_layer_collection, state):
    """Set exclusion state while preserving children state."""
    # Get current child exclusion state
    child_exclusion = []

    def get_child_exclusion(layer_collection):
        child_exclusion.append([layer_collection, layer_collection.exclude])

    apply_to_children(target_layer_collection, get_child_exclusion)

    # Set exclusion
    target_layer_collection.exclude = state

    # Restore correct state for all children
    for laycol in child_exclusion:
        laycol[0].exclude = laycol[1]
