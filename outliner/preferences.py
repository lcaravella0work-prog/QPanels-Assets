# SPDX-FileCopyrightText: 2011 Ryan Inch
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    CollectionProperty,
    BoolProperty,
    StringProperty,
    IntProperty,
)

from . import internals


class QPanelOutlinerProperties(PropertyGroup):
    qpo_list_collection: CollectionProperty(type=internals.QPOutlinerListCollection)
    qpo_list_index: IntProperty()

    show_exclude: BoolProperty(default=True, name="[EC] Exclude from View Layer")
    show_selectable: BoolProperty(default=True, name="[SS] Disable Selection")
    show_hide_viewport: BoolProperty(default=True, name="[VV] Hide in Viewport")
    show_disable_viewport: BoolProperty(default=False, name="[DV] Disable in Viewports")
    show_render: BoolProperty(default=False, name="[RR] Disable in Renders")
    show_holdout: BoolProperty(default=False, name="[HH] Holdout")
    show_indirect_only: BoolProperty(default=False, name="[IO] Indirect Only")

    align_local_ops: BoolProperty(default=False, name="Align Local Options",
                                  description="Align local options in a column to the right")

    in_phantom_mode: BoolProperty(default=False)

    ui_separator: StringProperty(name="", default="")
