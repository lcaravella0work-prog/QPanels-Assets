# QPanel Assets

Custom panels package for QPanel addon system.

## Features

### QPanel Outliner v1.0.0

Advanced collection manager for Blender with powerful organization and visibility controls.

**Key Features:**
- **Tree View Interface**: Hierarchical collection view with expand/collapse controls
- **Bulk Operations**: Apply visibility and selection settings to multiple collections
- **Smart Selection**: Filter collections by selected objects
- **Restriction Toggles** (RTOs):
  - Exclude from View Layer
  - Disable Selection
  - Hide in Viewport
  - Disable in Viewports
  - Disable in Renders
  - Holdout
  - Indirect Only
- **Collection Management**: Add, remove, rename collections
- **Object Management**: Send objects to collections with shift-click to add/remove
- **History System**: Undo/Redo with collection state preservation
- **Phantom Mode**: Preview RTO changes without committing

**Usage:**
1. Open QPanel Outliner from the QPanel menu
2. Use the tree view to navigate your collections
3. Click restriction toggle icons to control visibility
4. Use modifiers for advanced operations:
   - Shift+Click: Isolate/Restore
   - Ctrl+Click: Toggle nested collections
   - Shift+Ctrl+Click: Isolate with children
   - Alt+Click: Discard history

**Installation:**
This package is automatically loaded by QPanel when placed in the qpanel-assets folder.

## Version History

### 1.0.0 (2026-01-13)
- Initial release
- Full collection management
- All restriction toggles
- History and undo support
- Phantom mode

## License

Based on Collection Manager by Ryan Inch
Licensed under GPL-2.0-or-later
