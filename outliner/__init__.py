# SPDX-FileCopyrightText: 2011 Ryan Inch
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""
QPanel Outliner Module
Advanced collection manager for Blender
"""

if "bpy" in locals():
    import importlib

    importlib.reload(internals)
    importlib.reload(operator_utils)
    importlib.reload(operators)
    importlib.reload(ui)
    importlib.reload(preferences)

else:
    from . import internals
    from . import operator_utils
    from . import operators
    from . import ui
    from . import preferences

import bpy
from bpy.app.handlers import persistent
from bpy.props import PointerProperty


classes = (
    internals.QPOutlinerListCollection,
    internals.QPOutlinerSendReport,
    internals.QPOutlinerUISeparatorButton,
    operators.SetActiveCollection,
    operators.ExpandAllOperator,
    operators.ExpandSublevelOperator,
    operators.QPOutlinerExcludeOperator,
    operators.QPOutlinerUnExcludeAllOperator,
    operators.QPOutlinerRestrictSelectOperator,
    operators.QPOutlinerUnRestrictSelectAllOperator,
    operators.QPOutlinerHideOperator,
    operators.QPOutlinerUnHideAllOperator,
    operators.QPOutlinerDisableViewportOperator,
    operators.QPOutlinerUnDisableViewportAllOperator,
    operators.QPOutlinerDisableRenderOperator,
    operators.QPOutlinerUnDisableRenderAllOperator,
    operators.QPOutlinerHoldoutOperator,
    operators.QPOutlinerUnHoldoutAllOperator,
    operators.QPOutlinerIndirectOnlyOperator,
    operators.QPOutlinerUnIndirectOnlyAllOperator,
    operators.QPOutlinerNewCollectionOperator,
    operators.QPOutlinerRemoveCollectionOperator,
    operators.QPOutlinerRemoveEmptyCollectionsOperator,
    operators.QPOutlinerSelectCollectionObjectsOperator,
    operators.SelectAllCumulativeObjectsOperator,
    operators.QPOutlinerSendObjectsToCollectionOperator,
    operators.QPOutlinerPhantomModeOperator,
    operators.QPOutlinerApplyPhantomModeOperator,
    operators.QPOutlinerUndoWrapper,
    operators.QPOutlinerRedoWrapper,
    preferences.QPanelOutlinerProperties,
    ui.QPO_UL_items,
    ui.QPanelOutliner,
    ui.QPOutlinerDisplayOptionsPanel,
    ui.SpecialsMenu,
    )


@persistent
def depsgraph_update_post_handler(dummy):
    if internals.move_triggered:
        internals.move_triggered = False
        return

    internals.move_selection.clear()
    internals.move_active = None

@persistent
def undo_redo_post_handler(dummy):
    internals.move_selection.clear()
    internals.move_active = None


@persistent
def global_load_pre_handler(dummy):
    internals.move_triggered = False
    internals.move_selection.clear()
    internals.move_active = None


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.qpanel_outliner = PointerProperty(type=preferences.QPanelOutlinerProperties)

    bpy.app.handlers.depsgraph_update_post.append(depsgraph_update_post_handler)
    bpy.app.handlers.undo_post.append(undo_redo_post_handler)
    bpy.app.handlers.redo_post.append(undo_redo_post_handler)
    bpy.app.handlers.load_pre.append(global_load_pre_handler)


def unregister():
    bpy.app.handlers.load_pre.remove(global_load_pre_handler)
    bpy.app.handlers.redo_post.remove(undo_redo_post_handler)
    bpy.app.handlers.undo_post.remove(undo_redo_post_handler)
    bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update_post_handler)

    del bpy.types.Scene.qpanel_outliner

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
