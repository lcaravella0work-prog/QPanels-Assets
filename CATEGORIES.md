# QPanel Assets - Categories v2.1.0

Complete collection of essential Blender panels based on bl_ui.

## 🎬 **Animation**

### space_dopesheet.py
- Dopesheet Filters
- Keyframe Tools (Insert/Delete)
- Timeline Playback
- Action Editor

### space_graph.py
- Graph View Settings
- F-Curve Modifiers (Noise, Cycles, Limits, Envelope)
- Interpolation (Constant, Linear, Bezier)
- Handle Types

### space_nla.py
- NLA Tracks Manager
- Strip Tools (Add/Duplicate/Delete)

## 🎨 **Rendering & Output**

### properties_render.py
- Render Settings (Engine selection, Samples)
- Output (Resolution, Frame Rate)
- File Format (PNG, JPEG, compression)
- Sampling (Cycles adaptive sampling)

## 🖼️ **3D View**

### view3d.py (v2.0)
- Transform (Location, Rotation, Scale)
- Snapping (Settings and options)
- View Properties (Lens, clip distances)
- Overlays (Grid, axes, guides)

## 📦 **Object Properties**

### properties.py (v2.0)
- Modifiers (List with toggles)
- Materials (Slots and preview)
- Object Data (Statistics)
- Constraints (List and settings)

## 🔷 **Mesh**

### properties_data_mesh.py
- Mesh Data (Vertex/Edge/Face counts)
- Normals (Auto Smooth, Flip, Recalculate)
- Vertex Groups
- Shape Keys
- UV Maps

## 📷 **Camera**

### properties_data_camera.py
- Camera Lens (Focal Length, Type: Persp/Ortho)
- Depth of Field (Focus, F-Stop)
- Viewport Display (Limits, Mist, Sensor)
- Safe Areas (Title, Action)

## 💡 **Light**

### properties_data_light.py
- Light Settings (Type, Color, Power, Specular)
- Shadow (Cast Shadows, Softness)
- Spot Shape (Size, Blend, Show Cone)
- Area Shape (Square, Rectangle, Disk, Ellipse)

## 🌀 **Curve**

### properties_data_curve.py
- Curve Shape (Dimensions, Resolution)
- Geometry (Bevel Depth/Resolution, Extrude, Offset)
- Path Animation (Enable Path, Frames, Follow)

## 🦴 **Armature**

### properties_data_armature.py
- Armature Bones (Count, Active bone)
- Viewport Display (Display Type, Names, Axes, Shapes)
- Pose Options (Select, Copy/Paste Pose)

## ✨ **Particles**

### properties_particle.py
- Particle System (Type: Emitter/Hair, Count)
- Emission (Emit From, Normal/Tangent factors)
- Velocity (Randomize, Object velocity)
- Render (Object/Collection instances)

## 🔮 **Physics**

### properties_physics.py
- Rigid Body (Type: Active/Passive, Mass, Friction, Bounciness)
- Cloth (Quality Steps, Mass, Tension, Bending)
- Collision (Damping, Thickness, Friction)
- Fluid

## 🌍 **Scene & World**

### properties_scene.py
- Units (System, Scale, Length unit)
- Gravity (Force vector for physics)
- Audio (Sync, Scrubbing, Volume)
- World Surface (Use Nodes, Background Color)
- Viewport Display

## 🖼️ **UV / Image Editor**

### space_image.py
- Image View (Stereo 3D, Repeat)
- UV Selection (Box, Circle, Lasso, Linked, More/Less)
- UV Transform (Move, Rotate, Scale, Pin, Unwrap)
- Texture Paint (Mode, Brush: Size, Strength, Blend)

## 🎨 **Shader / Node Editor**

### space_node.py
- Node Tree Info (Active material)
- Add Shader (Principled BSDF, Diffuse, Glossy, Emission, Mix)
- Add Texture (Image, Noise, Voronoi, Wave)
- Color & Vector (RGB, ColorRamp, Mix, Hue/Sat, Mapping, Normal Map, Bump)
- Converters (Math, Separate/Combine XYZ/RGB)

## 🎞️ **Video Sequencer**

### space_sequencer.py
- Strip Tools (Add: Movie, Image, Sound; Edit: Split, Delete, Duplicate)
- Effects (Cross, Wipe, Color Mix, Transform, Glow)
- Preview (Frame control, Play/Stop)

## 🖌️ **Texture**

### properties_texture.py
- Texture Settings
- Image Texture (List all loaded images with resolution)
- Mapping (Coordinate systems: Generated, UV, Object, Camera, Window, Normal)

## 🌳 **Outliner**

### outliner.py (v2.0)
- Complete scene hierarchy
- Collections tree (Scene Collection + nested)
- Object parent/child relationships
- Visibility toggles

---

## 📊 **Statistics**
- **16 modules**
- **60+ panels**
- **Full bl_ui coverage** of essential Blender workflows

## 🔄 **Auto-Discovery**
Drop any `.py` file in `panels/` → Automatically loaded and registered.  
No manual imports needed!

## ✅ **Based on Blender 5.0 bl_ui**
All panels recreated from native Blender source for maximum compatibility.
