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

## 📋 Available Panels (v2.1.6)

### ✅ Properties Panels (11)
- **Properties**: Main properties panel
- **Armature Properties**: Armature data settings
- **Camera Properties**: Camera configuration
- **Curve Properties**: Curve and bezier settings
- **Light Properties**: Light source properties
- **Mesh Properties**: Mesh data settings
- **Particle Properties**: Particle systems
- **Physics Properties**: Physics simulations
- **Render Properties**: Render settings
- **Scene Properties**: Scene configuration
- **Texture Properties**: Texture management

### ✅ Space Panels (7)
- **Dope Sheet**: Animation timeline
- **Graph Editor**: Animation curves and F-curves
- **Image Editor**: UV/Image editing workspace
- **NLA Editor**: Non-linear animation
- **Node Editor**: Shader and geometry nodes
- **Sequencer**: Video sequence editor
- **3D View**: 3D viewport tools

### ⚠️ Archived Panels
- **Outliner** (v2.1.5): Archived due to non-functional state. See branch `archive/outliner-v2.1.5-non-functional` for reference.

**Total Active Panels**: 18 functional panels

**Usage:**
1. Open Panel Selector (Alt+F2)
2. Select any panel from the list
3. Assign to QPanel slot (F1-F12)
4. Access instantly via keyboard shortcut

## 🔄 Updates

QPanels automatically checks for updates every 5 minutes.

**Manual update:**
1. **Edit > Preferences > Add-ons > QPanels > License**
2. Click **"Check for Updates"**
3. If available, click **"Update to vX.X.X"**

## 📂 Structure

```
QPanels-Assets/
├── __init__.py           # Entry point (deprecated - panels/ handles registration)
├── version.json          # Version metadata
├── CATEGORIES.md         # Panel categorization
├── README.md             # Documentation
└── panels/               # All panel modules
    ├── __init__.py       # Auto-registration system
    ├── properties.py
    ├── properties_data_*.py (armature, camera, curve, light, mesh)
    ├── properties_particle.py
    ├── properties_physics.py
    ├── properties_render.py
    ├── properties_scene.py
    ├── properties_texture.py
    ├── space_dopesheet.py
    ├── space_graph.py
    ├── space_image.py
    ├── space_nla.py
    ├── space_node.py
    ├── space_sequencer.py
    └── view3d.py
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

**v5.4.0 Panels Restoration:**
- Original QPanels v5.4.0 panels by Lucas Caravella
- Restored to QPanels-Assets v2.1.6 (2026-01-15)
- Original: https://github.com/ryan-inch/Blender-Collection-Manager
- License: GPL-3.0-or-later
- Modifications: Removed QCD system, adapted for QPanels popup workflow

---

**Version:** 1.0.0  
**Last Updated:** January 13, 2026  
**Blender Compatibility:** 3.4.0+  
**QPanels Compatibility:** 6.2.0+
