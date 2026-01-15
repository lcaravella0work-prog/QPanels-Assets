## [2.1.5] - 2026-01-15

### 🔥 Fixed - CRITICAL RUNTIME ERROR
- **BUG**: `bpy_struct.__new__(struct): expected a single argument`
  - Cause: Panel wrapper tried to instantiate Operator with `QPANEL_ASSET_OT_collection_outliner()`
  - Blender classes (`Operator`, `Panel`) inherit from `bpy_struct` and cannot be instantiated directly
  - Console: `[QPanels] Error drawing panel 'QPANEL_ASSET_PT_outliner'` (repeated on every draw)
  - Impact: Panel appeared in selector but crashed when opened

### ✅ Solution - Shared Helper Function Architecture
- **NEW**: `draw_collection_outliner_ui(layout, context, master_collection_prop=None)`
  - Extracts all UI code (150+ lines) into shared function
  - Location: `panels/outliner/ui.py` (before Operator class)
  - Parameters:
    * `layout`: Blender UILayout to render into
    * `context`: Blender context
    * `master_collection_prop`: Optional - Operator instance for master collection name property

### 🔧 Changed
- **Operator.draw()**: Now calls `draw_collection_outliner_ui(self.layout, context, master_collection_prop=self)`
  - 3 lines instead of 130+ lines
  - Passes `self` for master collection property access
- **Panel.draw()**: Now calls `draw_collection_outliner_ui(self.layout, context)`
  - 2 lines instead of attempting Operator instantiation
  - No master collection property (displays static "Scene Collection" label)

### 🏗️ Architecture Benefits
- ✅ **Zero Code Duplication**: UI code exists once, used by both Panel and Operator
- ✅ **Proper Separation**: Helper function = pure UI logic, no bpy_struct instantiation
- ✅ **Maintainability**: UI changes in one place affect both Panel and Operator
- ✅ **Performance**: No attempted object creation on every draw call

### 📊 Expected Result
- **Before v2.1.5**: Panel visible but crashed with bpy_struct error
- **After v2.1.5**: Panel opens correctly, displays collection tree, all operators functional
- **Tested**: Works in all Blender areas (3D View, Image Editor, etc.)

---

## [2.1.4] - 2026-01-15

### 🔥 Fixed - CRITICAL PANEL DETECTION
- **ROOT CAUSE IDENTIFIED**: Outliner was an Operator (`QPANEL_ASSET_OT_outliner`), not a Panel
  - QPanels Panel Selector **only detects `bpy.types.Panel` subclasses** via `issubclass()` introspection
  - Console showed `Panel classes before: 1235 → after: 1235` (diff = 0, no Panel registered)
  - Result: Outliner invisible in Panel Selector despite successful installation

### ✅ Added
- **NEW**: `QPANEL_ASSET_PT_outliner` (Panel wrapper class)
  - Inherits from `bpy.types.Panel` (required for QPanels detection)
  - Attributes: `bl_qpanel_category = "OUTLINER"`, `bl_region_type = 'WINDOW'`
  - Method `draw()` delegates to existing Operator implementation (no code duplication)
  - Location: `panels/outliner/ui.py`

### 🔧 Changed
- **KEPT**: `QPANEL_ASSET_OT_outliner` (Operator) for standalone usage
  - Still works with `wm.invoke_popup()` for direct calls
  - UI implementation unchanged (200+ lines)
- **Registration order**: Panel registered BEFORE Operator in `panels/__init__.py`
- **Exports**: Added `QPANEL_ASSET_PT_outliner` to `panels/outliner/__init__.py`

### 📊 Expected Result
- Console: `Panel classes before: 1235 → after: 1236` (diff = +1)
- Panel Selector: `🌳 OUTLINER > Collection Outliner` now visible
- Pattern: Dual implementation (Panel wrapper + Operator) for maximum compatibility

---

## [2.1.1] - 2026-01-15

###  Fixed
- **CRITICAL**: Added class name alias `QPANEL_ASSET_OT_outliner` in `panels/outliner/ui.py`
  - Fixes ImportError: `cannot import name 'QPANEL_ASSET_OT_outliner'`
  - The actual class is `QPANEL_ASSET_OT_collection_outliner`, alias ensures compatibility
  - Resolves red Install button issue in QPanels UI

###  Changed
- Lowered `qpanels_min_version` from 6.2.0 to 6.1.19 for broader compatibility
- Panel Outliner version bumped to 1.0.1

---

# Changelog - QPanels Assets

All notable changes to QPanels Assets will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-01-13

### 🎉 Initial Release

**Architecture:**
- ✅ Multi-repo structure (QPanels-Core + QPanels-Assets)
- ✅ Centralized registration system (`panels/__init__.py`)
- ✅ Version tracking with SHA256 checksum (`version.json`)
- ✅ Automated checksum calculation (`scripts/update_checksum.py`)
- ✅ Complete documentation (README.md + QPANELS_ASSETS_ARCHITECTURE.md)

**Panels:**
- ✅ **Outliner v1.0.0** (Collection Manager-inspired)
  - Hierarchical collection tree with expand/collapse
  - 7 Render/Viewport toggles (RTO): Exclude, Select, Hide, Disable, Render, Holdout, Indirect
  - Advanced operations: Isolate (Alt), Toggle children (Ctrl), Activate all (Shift)
  - 12 operators (collection actions + RTOs with modifiers)
  - UIList rendering with active collection highlighting
  - Object selection from collections

**Credits:**
- Outliner panel based on Collection Manager v2.24.11 by Ryan Inch
- Original: https://github.com/ryan-inch/Blender-Collection-Manager
- License: GPL-3.0-or-later
- Modifications: Removed QCD system (74% code reduction: 7,221 → 1,860 lines), adapted for QPanels popup workflow

**Technical Details:**
- Total code: 1,860 lines (Python)
- Total documentation: 606 lines (Markdown)
- SHA256 checksum: `5969977546e2e9b4e57d8dd1760a0b580b7b4567d048414142b3b78bb97667fe`
- Blender compatibility: 3.4.0+
- QPanels compatibility: 6.2.0+

**Files:**
- `__init__.py` (27 lines) - Entry point
- `version.json` (14 lines) - Version tracking
- `README.md` (130 lines) - User documentation
- `CHANGELOG.md` (this file)
- `scripts/update_checksum.py` (105 lines) - SHA256 automation
- `panels/__init__.py` (56 lines) - Registration
- `panels/outliner/__init__.py` (74 lines) - Module re-exports
- `panels/outliner/internals.py` (450 lines) - State management
- `panels/outliner/operator_utils.py` (530 lines) - RTO utilities
- `panels/outliner/operators.py` (470 lines) - 12 operators
- `panels/outliner/ui.py` (360 lines) - Main popup + UIList
- `panels/outliner/README.md` (250 lines) - Panel documentation

---

## [Unreleased]

### Planned Features

**Upcoming Panels:**
- **Advanced Search** - Advanced panel search functionality
- **Custom Toolbars** - Customizable toolbar panels
- **Node Editor Shortcuts** - Quick node access
- **Animation Helpers** - Bulk keyframe operations

**Roadmap:**
- Q1 2026: Advanced Search panel
- Q2 2026: Custom Toolbars panel
- Q3 2026: Node Editor Shortcuts
- Q4 2026: Animation Helpers

---

## Version History

| Version | Date | Panels | Lines of Code | SHA256 (first 8 chars) |
|---------|------|--------|---------------|------------------------|
| 1.0.0 | 2026-01-13 | Outliner | 1,860 | 59699775 |

---

**Repository:** [QPanels-Assets](https://github.com/lcaravella0work-prog/QPanels-Assets)  
**Documentation:** [QPANELS_ASSETS_ARCHITECTURE.md](https://github.com/lcaravella0work-prog/QPanels-Core/blob/main/docs/QPANELS_ASSETS_ARCHITECTURE.md)  
**License:** GPL-3.0-or-later

