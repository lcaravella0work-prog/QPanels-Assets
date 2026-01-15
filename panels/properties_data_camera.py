# -*- coding: utf-8 -*-
"""
QPanel Assets - Camera Data Properties
Camera settings, lens, and depth of field

Based on Blender's properties_data_camera.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_camera_lens(Panel):
    """Camera Lens Settings"""
    bl_label = "Camera Lens"
    bl_idname = "QPANEL_PT_camera_lens"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CAMERA'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CAMERA'
    
    def draw(self, context):
        layout = self.layout
        cam = context.active_object.data
        
        col = layout.column()
        col.prop(cam, "type", text="Type")
        
        if cam.type == 'PERSP':
            col.separator()
            col.prop(cam, "lens", text="Focal Length")
            col.prop(cam, "lens_unit", text="Unit")
        elif cam.type == 'ORTHO':
            col.prop(cam, "ortho_scale", text="Orthographic Scale")


class QPANEL_PT_camera_dof(Panel):
    """Camera Depth of Field"""
    bl_label = "Depth of Field"
    bl_idname = "QPANEL_PT_camera_dof"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CAMERA'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CAMERA'
    
    def draw(self, context):
        layout = self.layout
        cam = context.active_object.data
        dof = cam.dof
        
        col = layout.column()
        col.prop(dof, "use_dof", text="Enable DOF")
        
        if dof.use_dof:
            col.separator()
            col.prop(dof, "focus_object", text="Focus Object")
            col.prop(dof, "focus_distance", text="Focus Distance")
            col.prop(dof, "aperture_fstop", text="F-Stop")


class QPANEL_PT_camera_viewport(Panel):
    """Camera Viewport Display"""
    bl_label = "Viewport Display"
    bl_idname = "QPANEL_PT_camera_viewport"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CAMERA'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CAMERA'
    
    def draw(self, context):
        layout = self.layout
        cam = context.active_object.data
        
        col = layout.column()
        col.prop(cam, "show_limits", text="Limits")
        col.prop(cam, "show_mist", text="Mist")
        col.prop(cam, "show_sensor", text="Sensor")
        col.prop(cam, "show_name", text="Name")


class QPANEL_PT_camera_safe_areas(Panel):
    """Camera Safe Areas"""
    bl_label = "Safe Areas"
    bl_idname = "QPANEL_PT_camera_safe_areas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'CAMERA'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'CAMERA'
    
    def draw(self, context):
        layout = self.layout
        cam = context.active_object.data
        
        col = layout.column()
        col.prop(cam, "show_safe_areas", text="Show Safe Areas")
        
        if cam.show_safe_areas:
            col.separator()
            safe = cam.safe_areas
            col.prop(safe, "title", text="Title", slider=True)
            col.prop(safe, "action", text="Action", slider=True)


# Registration
classes = (
    QPANEL_PT_camera_lens,
    QPANEL_PT_camera_dof,
    QPANEL_PT_camera_viewport,
    QPANEL_PT_camera_safe_areas,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
