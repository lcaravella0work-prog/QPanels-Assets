# QPanels Assets

**Extension package for QPanels Core**  
Provides additional panels accessible via QPanels system.

## 📦 What is this?

QPanels Assets is **NOT a standalone add-on**. It's a downloadable package that extends QPanels Core with additional panels.

## 🚀 Installation

**Method 1: Via QPanels (Recommended)**

1. Install QPanels Core add-on in Blender
2. Open **Edit > Preferences > Add-ons > QPanels > License tab**
3. Click **"Install QPanels Assets"**
4. QPanels automatically downloads and installs this package

**Method 2: Manual Installation (Development)**

```bash
# Copy to Blender addons folder
cp -r QPanels-Assets/ "AppData/Roaming/Blender Foundation/Blender/<version>/scripts/addons/qpanel-assets/"
```

## 📋 Available Panels

### Outliner (v1.0.0)
Collection Manager-inspired popup for managing Blender collections.

**Features:**
- Hierarchical collection tree with expand/collapse
- 7 Render/Viewport toggles (RTO): Exclude, Select, Hide, Disable, Render, Holdout, Indirect
- Advanced operations: Isolate (Alt), Toggle children (Ctrl), Activate all (Shift)
- Object selection from collections
- Active collection highlighting

**Usage:**
1. Open Panel Selector (Alt+F2)
2. Select "Outliner" → Assign to QPanel 1
3. Press F1 (or your assigned key) → Outliner popup appears

**Attribution:**
Based on Collection Manager v2.24.11 by Ryan Inch (GPL-3.0)

## 🔄 Updates

QPanels automatically checks for updates every 5 minutes.

**Manual update:**
1. **Edit > Preferences > Add-ons > QPanels > License**
2. Click **"Check for Updates"**
3. If available, click **"Update to vX.X.X"**

## 📂 Structure

```
QPanels-Assets/
├── __init__.py           # Entry point
├── version.json          # Version tracking
├── README.md             # This file
└── panels/               # All panels
    ├── __init__.py       # Central registration
    └── outliner/         # Outliner panel
        ├── __init__.py
        ├── ui.py
        ├── operators.py
        ├── operator_utils.py
        ├── internals.py
        └── README.md
```

## 🛠️ Development

**Adding a new panel:**

1. Create folder `panels/<panel_name>/`
2. Add panel operator with `bl_qpanel_category = "QPanels Assets"`
3. Import in `panels/__init__.py`
4. Update `version.json`
5. Test locally, then push to GitHub

See [QPANELS_ASSETS_ARCHITECTURE.md](../QPanels-Core/docs/QPANELS_ASSETS_ARCHITECTURE.md) for complete guide.

## 📄 License

GPL-3.0-or-later (compatible with Blender)

Individual panels may include code from other GPL-compatible add-ons (with proper attribution).

## 🔗 Links

- [QPanels Core Repository](https://github.com/lcaravella0work-prog/QPanels-Core)
- [QPanels Assets Repository](https://github.com/lcaravella0work-prog/QPanels-Assets)
- [Documentation](https://github.com/lcaravella0work-prog/QPanels-Core/tree/main/docs)

## ⚖️ Credits

**Outliner Panel:**
- Based on Collection Manager v2.24.11 by Ryan Inch
- Original: https://github.com/ryan-inch/Blender-Collection-Manager
- License: GPL-3.0-or-later
- Modifications: Removed QCD system, adapted for QPanels popup workflow

---

**Version:** 1.0.0  
**Last Updated:** January 13, 2026  
**Blender Compatibility:** 3.4.0+  
**QPanels Compatibility:** 6.2.0+
