# -*- coding: utf-8 -*-
"""
QPanel Assets - Curve Data Properties
Curve editing, bezier, NURBS, and path settings

Based on Blender's properties_data_curve.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_curve_shape(Panel):
    """Curve Shape Settings"""
    bl_label = "Curve Shape"
    bl_idname = "QPANEL_PT_curve_shape"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CURVE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type in {'CURVE', 'CURVES'}
    
    def draw(self, context):
        layout = self.layout
        curve = context.active_object.data
        
        col = layout.column()
        col.prop(curve, "dimensions", text="Dimensions")
        col.prop(curve, "resolution_u", text="Resolution")
        col.prop(curve, "render_resolution_u", text="Render Resolution")


class QPANEL_PT_curve_geometry(Panel):
    """Curve Geometry Settings"""
    bl_label = "Geometry"
    bl_idname = "QPANEL_PT_curve_geometry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CURVE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CURVE'
    
    def draw(self, context):
        layout = self.layout
        curve = context.active_object.data
        
        col = layout.column()
        col.label(text="Bevel:", icon='MOD_BEVEL')
        col.prop(curve, "bevel_depth", text="Depth")
        col.prop(curve, "bevel_resolution", text="Resolution")
        
        layout.separator()
        col = layout.column()
        col.prop(curve, "extrude", text="Extrude")
        col.prop(curve, "offset", text="Offset")


class QPANEL_PT_curve_path(Panel):
    """Curve Path Animation"""
    bl_label = "Path Animation"
    bl_idname = "QPANEL_PT_curve_path"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CURVE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CURVE'
    
    def draw(self, context):
        layout = self.layout
        curve = context.active_object.data
        
        col = layout.column()
        col.prop(curve, "use_path", text="Enable Path")
        
        if curve.use_path:
            col.separator()
            col.prop(curve, "path_duration", text="Frames")
            col.prop(curve, "use_path_follow", text="Follow")


# Registration
classes = (
    QPANEL_PT_curve_shape,
    QPANEL_PT_curve_geometry,
    QPANEL_PT_curve_path,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
