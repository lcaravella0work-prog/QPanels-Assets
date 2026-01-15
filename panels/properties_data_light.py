# -*- coding: utf-8 -*-
"""
QPanel Assets - Light Data Properties
Light settings, color, and shadows

Based on Blender's properties_data_light.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_light_settings(Panel):
    """Light Settings"""
    bl_label = "Light Settings"
    bl_idname = "QPANEL_PT_light_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'LIGHT'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'LIGHT'
    
    def draw(self, context):
        layout = self.layout
        light = context.active_object.data
        
        col = layout.column()
        col.prop(light, "type", text="Type")
        
        col.separator()
        col.prop(light, "color", text="Color")
        col.prop(light, "energy", text="Power")
        col.prop(light, "specular_factor", text="Specular")


class QPANEL_PT_light_shadow(Panel):
    """Light Shadow Settings"""
    bl_label = "Shadow"
    bl_idname = "QPANEL_PT_light_shadow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'LIGHT'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'LIGHT'
    
    def draw(self, context):
        layout = self.layout
        light = context.active_object.data
        
        col = layout.column()
        col.prop(light, "use_shadow", text="Cast Shadows")
        
        if light.use_shadow:
            col.separator()
            if light.type in {'POINT', 'SPOT', 'SUN'}:
                col.prop(light, "shadow_soft_size", text="Softness")


class QPANEL_PT_light_spot(Panel):
    """Spot Light Settings"""
    bl_label = "Spot Shape"
    bl_idname = "QPANEL_PT_light_spot"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'LIGHT'
    
    @classmethod
    def poll(cls, context):
        return (context.active_object and 
                context.active_object.type == 'LIGHT' and 
                context.active_object.data.type == 'SPOT')
    
    def draw(self, context):
        layout = self.layout
        light = context.active_object.data
        
        col = layout.column()
        col.prop(light, "spot_size", text="Size")
        col.prop(light, "spot_blend", text="Blend", slider=True)
        col.prop(light, "show_cone", text="Show Cone")


class QPANEL_PT_light_area(Panel):
    """Area Light Settings"""
    bl_label = "Area Shape"
    bl_idname = "QPANEL_PT_light_area"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'LIGHT'
    
    @classmethod
    def poll(cls, context):
        return (context.active_object and 
                context.active_object.type == 'LIGHT' and 
                context.active_object.data.type == 'AREA')
    
    def draw(self, context):
        layout = self.layout
        light = context.active_object.data
        
        col = layout.column()
        col.prop(light, "shape", text="Shape")
        
        if light.shape in {'SQUARE', 'DISK'}:
            col.prop(light, "size", text="Size")
        elif light.shape in {'RECTANGLE', 'ELLIPSE'}:
            col.prop(light, "size", text="Size X")
            col.prop(light, "size_y", text="Size Y")


# Registration
classes = (
    QPANEL_PT_light_settings,
    QPANEL_PT_light_shadow,
    QPANEL_PT_light_spot,
    QPANEL_PT_light_area,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
