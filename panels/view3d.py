# -*- coding: utf-8 -*-
"""
QPanel Assets - Transform & View Panels
Essential 3D View panels (Transform, Snapping, View Properties)

Based on Blender's native space_view3d.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_transform(Panel):
    """Transform Tools - Location, Rotation, Scale"""
    bl_label = "Transform"
    bl_idname = "QPANEL_PT_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'VIEWPORT'
    
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        layout.label(text=obj.name, icon='OBJECT_DATA')
        layout.separator()
        
        col = layout.column()
        col.prop(obj, "location")
        col.prop(obj, "rotation_euler")
        col.prop(obj, "scale")


class QPANEL_PT_snapping(Panel):
    """Snapping Options"""
    bl_label = "Snapping"
    bl_idname = "QPANEL_PT_snapping"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'VIEWPORT'
    
    def draw(self, context):
        layout = self.layout
        tool_settings = context.tool_settings
        
        col = layout.column()
        col.prop(tool_settings, "use_snap", text="Enable Snapping")
        
        if tool_settings.use_snap:
            col.separator()
            col.prop(tool_settings, "snap_elements", expand=True)
            col.prop(tool_settings, "snap_target")
            
            if 'FACE' in tool_settings.snap_elements:
                col.prop(tool_settings, "use_snap_align_rotation")
                col.prop(tool_settings, "use_snap_project")


class QPANEL_PT_view3d_properties(Panel):
    """3D View Properties"""
    bl_label = "View Properties"
    bl_idname = "QPANEL_PT_view3d_properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'VIEWPORT'
    
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        
        col = layout.column()
        col.prop(view, "lens")
        col.prop(view, "clip_start", text="Clip Start")
        col.prop(view, "clip_end", text="Clip End")
        
        layout.separator()
        layout.prop(view, "lock_camera")
        layout.prop(view, "lock_cursor")


class QPANEL_PT_overlay(Panel):
    """Viewport Overlay Options"""
    bl_label = "Overlays"
    bl_idname = "QPANEL_PT_overlay"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'VIEWPORT'
    
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        overlay = view.overlay
        
        col = layout.column()
        col.separator()
        col.prop(overlay, "show_floor", text="Grid Floor")
        col.prop(overlay, "show_axis_x", text="X Axis")
        col.prop(overlay, "show_axis_y", text="Y Axis")
        col.prop(overlay, "show_axis_z", text="Z Axis")
        col.separator()
        col.prop(overlay, "show_cursor")
        col.prop(overlay, "show_object_origins")
        col.prop(overlay, "show_relationship_lines")


# Classes to register
classes = (
    QPANEL_PT_transform,
    QPANEL_PT_snapping,
    QPANEL_PT_view3d_properties,
    QPANEL_PT_overlay,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

