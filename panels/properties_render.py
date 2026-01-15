# -*- coding: utf-8 -*-
"""
QPanel Assets - Render Properties
Render settings, output, and performance

Based on Blender's properties_render.py & properties_output.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_render_settings(Panel):
    """Render Settings"""
    bl_label = "Render Settings"
    bl_idname = "QPANEL_PT_render_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'RENDERING'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render
        
        col = layout.column()
        col.prop(rd, "engine", text="Render Engine")
        
        col.separator()
        col.prop(scene.eevee if hasattr(scene, 'eevee') else rd, "taa_render_samples", text="Samples")


class QPANEL_PT_render_output(Panel):
    """Render Output Settings"""
    bl_label = "Output"
    bl_idname = "QPANEL_PT_render_output"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'RENDERING'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render
        
        col = layout.column()
        col.label(text="Resolution:", icon='OUTPUT')
        row = col.row(align=True)
        row.prop(rd, "resolution_x", text="X")
        row.prop(rd, "resolution_y", text="Y")
        col.prop(rd, "resolution_percentage", text="%")
        
        col.separator()
        col.prop(rd, "fps", text="Frame Rate")


class QPANEL_PT_render_format(Panel):
    """Render File Format"""
    bl_label = "File Format"
    bl_idname = "QPANEL_PT_render_format"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'RENDERING'
    
    def draw(self, context):
        layout = self.layout
        rd = context.scene.render
        image_settings = rd.image_settings
        
        col = layout.column()
        col.prop(rd, "filepath", text="")
        
        col.separator()
        col.prop(image_settings, "file_format", text="Format")
        
        if image_settings.file_format in {'PNG', 'JPEG', 'TIFF'}:
            col.prop(image_settings, "color_mode", text="Color")
            
            if image_settings.file_format == 'PNG':
                col.prop(image_settings, "compression", text="Compression")
            elif image_settings.file_format == 'JPEG':
                col.prop(image_settings, "quality", text="Quality")


class QPANEL_PT_render_sampling(Panel):
    """Render Sampling (Cycles)"""
    bl_label = "Sampling"
    bl_idname = "QPANEL_PT_render_sampling"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'RENDERING'
    
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'CYCLES'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        cycles = scene.cycles
        
        col = layout.column()
        col.prop(cycles, "samples", text="Render Samples")
        col.prop(cycles, "preview_samples", text="Viewport Samples")
        
        col.separator()
        col.prop(cycles, "use_adaptive_sampling", text="Adaptive Sampling")
        if cycles.use_adaptive_sampling:
            col.prop(cycles, "adaptive_threshold", text="Noise Threshold")


# Registration
classes = (
    QPANEL_PT_render_settings,
    QPANEL_PT_render_output,
    QPANEL_PT_render_format,
    QPANEL_PT_render_sampling,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
