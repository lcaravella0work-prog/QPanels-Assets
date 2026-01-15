# -*- coding: utf-8 -*-
"""
QPanel Assets - Image/UV Editor Panels
UV editing, painting, and image tools

Based on Blender's space_image.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_image_view(Panel):
    """Image View Settings"""
    bl_label = "View"
    bl_idname = "QPANEL_PT_image_view"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'IMAGE'

    
    def draw(self, context):
        layout = self.layout
        sima = context.space_data if hasattr(context, 'space_data') else None
        
        if sima and sima.image:
            layout.prop(sima, "show_stereo_3d")
            layout.prop(sima, "show_repeat")
            layout.separator()
        
        col = layout.column()
        col.label(text="Display")
        col.prop(context.preferences.view, "show_layout_ui", text="Show Sidebar")


class QPANEL_PT_uv_select(Panel):
    """UV Selection Tools"""
    bl_label = "UV Selection"
    bl_idname = "QPANEL_PT_uv_select"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'IMAGE'
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.active_object
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Selection Mode:")
        col.operator("uv.select_all", text="All").action = 'SELECT'
        col.operator("uv.select_all", text="None").action = 'DESELECT'
        col.operator("uv.select_all", text="Invert").action = 'INVERT'
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("uv.select_box", text="Box Select")
        col.operator("uv.select_circle", text="Circle Select")
        col.operator("uv.select_lasso", text="Lasso Select")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("uv.select_linked", text="Select Linked")
        col.operator("uv.select_more", text="Select More")
        col.operator("uv.select_less", text="Select Less")


class QPANEL_PT_uv_transform(Panel):
    """UV Transform Tools"""
    bl_label = "UV Transform"
    bl_idname = "QPANEL_PT_uv_transform"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'IMAGE'
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH' and context.active_object
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Operations:")
        col.operator("transform.translate", text="Move")
        col.operator("transform.rotate", text="Rotate")
        col.operator("transform.resize", text="Scale")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("uv.pin")
        col.operator("uv.unwrap")
        col.operator("uv.smart_project", text="Smart UV Project")


class QPANEL_PT_paint_image(Panel):
    """Texture Paint Settings"""
    bl_label = "Texture Paint"
    bl_idname = "QPANEL_PT_paint_image"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'IMAGE'
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'PAINT_TEXTURE' and context.active_object
    
    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings
        ipaint = toolsettings.image_paint
        
        col = layout.column()
        col.prop(ipaint, "mode", text="Mode")
        
        layout.separator()
        brush = toolsettings.image_paint.brush
        if brush:
            col = layout.column()
            col.label(text="Brush Settings:")
            col.prop(brush, "size", text="Size")
            col.prop(brush, "strength", text="Strength")
            col.prop(brush, "blend", text="Blend")


# Registration
classes = (
    QPANEL_PT_image_view,
    QPANEL_PT_uv_select,
    QPANEL_PT_uv_transform,
    QPANEL_PT_paint_image,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
