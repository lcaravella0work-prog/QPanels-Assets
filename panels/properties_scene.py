# -*- coding: utf-8 -*-
"""
QPanel Assets - Scene Properties
Scene settings, units, and world

Based on Blender's properties_scene.py & properties_world.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_scene_units(Panel):
    """Scene Units"""
    bl_label = "Units"
    bl_idname = "QPANEL_PT_scene_units"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SCENE'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        unit = scene.unit_settings
        
        col = layout.column()
        col.prop(unit, "system", text="Unit System")
        col.prop(unit, "scale_length", text="Unit Scale")
        col.prop(unit, "length_unit", text="Length")


class QPANEL_PT_scene_gravity(Panel):
    """Scene Gravity"""
    bl_label = "Gravity"
    bl_idname = "QPANEL_PT_scene_gravity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SCENE'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column()
        col.prop(scene, "gravity", text="")
        col.label(text="Gravity force for physics simulation")


class QPANEL_PT_scene_audio(Panel):
    """Scene Audio Settings"""
    bl_label = "Audio"
    bl_idname = "QPANEL_PT_scene_audio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SCENE'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render
        
        col = layout.column()
        col.prop(rd, "use_audio_sync", text="Audio Sync")
        col.prop(rd, "use_audio_scrub", text="Audio Scrubbing")
        
        col.separator()
        col.prop(scene, "audio_volume", text="Volume")


class QPANEL_PT_world_surface(Panel):
    """World Surface Settings"""
    bl_label = "World Surface"
    bl_idname = "QPANEL_PT_world_surface"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SCENE'
    
    def draw(self, context):
        layout = self.layout
        world = context.scene.world
        
        if world:
            col = layout.column()
            col.prop(world, "use_nodes", text="Use Nodes")
            
            if not world.use_nodes:
                col.separator()
                col.prop(world, "color", text="Color")
        else:
            layout.label(text="No world in scene", icon='INFO')


class QPANEL_PT_world_viewport(Panel):
    """World Viewport Display"""
    bl_label = "Viewport Display"
    bl_idname = "QPANEL_PT_world_viewport"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SCENE'
    
    def draw(self, context):
        layout = self.layout
        world = context.scene.world
        
        if world:
            col = layout.column()
            col.prop(world, "color", text="Background Color")
        else:
            layout.label(text="No world in scene", icon='INFO')


# Registration
classes = (
    QPANEL_PT_scene_units,
    QPANEL_PT_scene_gravity,
    QPANEL_PT_scene_audio,
    QPANEL_PT_world_surface,
    QPANEL_PT_world_viewport,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
