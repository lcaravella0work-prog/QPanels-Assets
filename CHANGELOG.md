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

