# SPDX-License-Identifier: GPL-3.0-or-later
# This file is part of QPanels Assets - Collection Outliner
# Original code from Collection Manager by Ryan Inch (https://github.com/ryan-inch/Collection-Manager)
# Adapted for QPanels Assets by QPanels Team

"""
QPanels Assets - Collection Outliner Module
Based on Collection Manager v2.24.11 by Ryan Inch

This module provides an advanced collection management popup for QPanels.
All operators and classes are re-exported for registration in panels/__init__.py
"""

import bpy

# Import all modules
from . import internals
from . import operator_utils
from . import operators
from . import ui

# Re-export all classes for registration
from .ui import (
    QPANEL_ASSET_OT_outliner,
    QPANEL_ASSET_UL_collection_tree,
    CollectionManagerProperties,
)

from .operators import (
    QPANEL_ASSET_OT_set_active_collection,
    QPANEL_ASSET_OT_expand_all_collections,
    QPANEL_ASSET_OT_expand_sublevel,
    QPANEL_ASSET_OT_select_collection_objects,
    QPANEL_ASSET_OT_rto_exclude_collection,
    QPANEL_ASSET_OT_rto_select_collection,
    QPANEL_ASSET_OT_rto_hide_collection,
    QPANEL_ASSET_OT_rto_disable_collection,
    QPANEL_ASSET_OT_rto_render_collection,
    QPANEL_ASSET_OT_rto_holdout_collection,
    QPANEL_ASSET_OT_rto_indirect_collection,
    QPANEL_ASSET_OT_remove_collection,
)

__all__ = [
    # Main popup operator
    "QPANEL_ASSET_OT_outliner",
    
    # UIList
    "QPANEL_ASSET_UL_collection_tree",
    
    # Properties
    "CollectionManagerProperties",
    
    # Collection operators
    "QPANEL_ASSET_OT_set_active_collection",
    "QPANEL_ASSET_OT_expand_all_collections",
    "QPANEL_ASSET_OT_expand_sublevel",
    "QPANEL_ASSET_OT_select_collection_objects",
    "QPANEL_ASSET_OT_remove_collection",
    
    # RTO operators
    "QPANEL_ASSET_OT_rto_exclude_collection",
    "QPANEL_ASSET_OT_rto_select_collection",
    "QPANEL_ASSET_OT_rto_hide_collection",
    "QPANEL_ASSET_OT_rto_disable_collection",
    "QPANEL_ASSET_OT_rto_render_collection",
    "QPANEL_ASSET_OT_rto_holdout_collection",
    "QPANEL_ASSET_OT_rto_indirect_collection",
]
