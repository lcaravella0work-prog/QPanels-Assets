# Collection Outliner - QPanels Assets

Advanced collection management panel for QPanels, inspired by [Collection Manager](https://github.com/ryan-inch/Collection-Manager) by Ryan Inch.

## Overview

This module integrates Collection Manager's powerful outliner functionality into QPanels Assets, providing a hierarchical tree view of collections with RTO (Restriction Toggle Operator) controls.

## Features

### Core Functionality
- **Hierarchical Tree View**: Expandable/collapsible collection tree with visual indentation
- **RTO Toggles**: Quick access to all Blender collection properties:
  - Exclude from View Layer
  - Selectability (hide_select)
  - Hide in Viewport
  - Disable in Viewport
  - Hide in Render
  - Holdout
  - Indirect Only

### Advanced Operations
- **Isolate Mode**: Quickly isolate collections (Alt+Click on RTO)
- **Batch Operations**: 
  - Shift+Click: Toggle all RTOs
  - Ctrl+Click: Toggle children
  - Ctrl+Shift+Click: Invert RTOs
  - Ctrl+Alt+Click: Copy/Paste RTO states
  - Ctrl+Shift+Alt+Click: Swap RTO states

- **Object Selection**: Click on collection to select/deselect all objects
  - Ctrl+Click: Nested selection
  - Shift+Click: Add/Remove from selection

- **Tree Navigation**:
  - Ctrl+Click expand icon: Expand/Collapse all sublevels
  - Shift+Click expand icon: Isolate tree branch
  - Alt+Click expand icon: Discard history

## Architecture

### File Structure

```
outliner/
├── __init__.py              # Registration entry point
├── internals.py             # Core state management (layer_collections, expanded, rto_history)
├── operator_utils.py        # RTO manipulation utilities
├── operators.py             # All operators (RTO toggles, collection management)
└── ui.py                    # Main popup + UIList rendering
```

### Key Components

#### internals.py
- **Global State**: 
  - `layer_collections`: Dict of all collections with metadata
  - `collection_tree`: Hierarchical tree structure
  - `expanded`: Set of expanded collection names
  - `rto_history`: Undo history for RTO operations

- **Functions**:
  - `update_collection_tree()`: Rebuild tree from view layer
  - `generate_state()`: Snapshot current collection states
  - `check_state()`: Detect external changes

#### operator_utils.py
- **RTO Manipulation**:
  - `get_rto()` / `set_rto()`: Safe getters/setters
  - `isolate_rto()`: Isolate collection with history
  - `toggle_children()`: Recursive toggle
  - `activate_all_rtos()`: Enable all with undo
  - `copy_rtos()` / `swap_rtos()`: Copy/paste states

#### operators.py
- **Collection Operations**:
  - `QPANEL_ASSET_OT_set_active_collection`: Set active layer collection
  - `QPANEL_ASSET_OT_expand_all`: Expand/collapse all
  - `QPANEL_ASSET_OT_expand_sublevel`: Expand specific level
  - `QPANEL_ASSET_OT_select_collection_objects`: Select objects in collection
  - `QPANEL_ASSET_OT_remove_collection`: Delete collection

- **RTO Operators**: (7 RTOs × multiple modifiers)
  - `QPANEL_ASSET_OT_toggle_exclude`
  - `QPANEL_ASSET_OT_toggle_select`
  - `QPANEL_ASSET_OT_toggle_hide`
  - `QPANEL_ASSET_OT_toggle_disable`
  - `QPANEL_ASSET_OT_toggle_render`
  - `QPANEL_ASSET_OT_toggle_holdout`
  - `QPANEL_ASSET_OT_toggle_indirect`

#### ui.py
- **Main Popup**: `QPANEL_ASSET_OT_collection_outliner`
  - View layer selector
  - Expand all button
  - Master collection row
  - Collection tree UIList

- **UIList**: `QPANEL_ASSET_UL_collection_tree`
  - Hierarchical rendering with indentation
  - Expand/collapse icons
  - Active collection highlighting
  - RTO toggle icons
  - Object selection indicator

## Removed from Original

This adaptation **removes** the QCD (Quick Collection Display) system from Collection Manager:
- **QCD Slots**: 20-slot quick access system
- **Phantom Mode**: Temporary visibility mode
- **QCD Operators**: ~3,100 lines of QCD-specific code
- **Persistent Data**: QCD slot storage across sessions

**Why?** QPanels Assets provides its own panel access system, making QCD redundant.

## Integration with QPanels Assets

### Detection
The main operator has `bl_qpanel_category = "Outliner"` marker for QPanels Assets detection.

### Invocation
QPanels will automatically detect this panel and make it available through the QPanels system.

```python
# QPanels Assets will call:
bpy.ops.qpanels_assets.collection_outliner('INVOKE_DEFAULT')
```

### Registration
Standard Blender add-on registration:
```python
from . import outliner

def register():
    outliner.register()

def unregister():
    outliner.unregister()
```

## Compatibility

- **Blender Version**: 3.4.0+
- **Python**: 3.10+
- **License**: GPL-3.0-or-later (same as original Collection Manager)
- **Dependencies**: None (pure Blender API)

## Credits

**Original Implementation**: [Ryan Inch](https://github.com/ryan-inch) - Collection Manager v2.24.11  
**Adaptation**: QPanels Team  
**License**: GPL-3.0-or-later

This module is a derivative work of Collection Manager, adapted for integration into QPanels Assets. All credit for the core implementation goes to Ryan Inch.

## Code Statistics

| Component         | Lines | Description                          |
|-------------------|-------|--------------------------------------|
| internals.py      | ~450  | State management, tree building      |
| operator_utils.py | ~530  | RTO manipulation utilities           |
| operators.py      | ~470  | Collection & RTO operators           |
| ui.py             | ~360  | Popup UI + UIList rendering          |
| __init__.py       | ~50   | Registration                         |
| **Total**         | ~1,860| **Clean, QCD-free implementation**   |

**Original Collection Manager**: 7,221 lines  
**Code Reduction**: 74% (removed QCD system)

## Usage Example

```python
# Invoke from QPanels
bpy.ops.qpanels_assets.collection_outliner('INVOKE_DEFAULT')

# Programmatic access to internals
from qpanel_assets.outliner import internals

# Get all collections
for name, laycol in internals.layer_collections.items():
    print(f"{name}: level {laycol['lvl']}")

# Check if collection is expanded
if "MyCollection" in internals.expanded:
    print("MyCollection is expanded")
```

## Future Enhancements

Potential improvements (not yet implemented):
- [ ] Filtering by name/type
- [ ] Drag & drop collection reordering
- [ ] Custom collection colors
- [ ] Collection templates
- [ ] Export/import collection hierarchy

## Support

For issues specific to this QPanels Assets integration, please report to QPanels repository.  
For issues with the underlying Collection Manager logic, refer to the [original repository](https://github.com/ryan-inch/Collection-Manager).
