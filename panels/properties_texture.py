# -*- coding: utf-8 -*-
"""
QPanel Assets - Texture Properties
Texture settings and image textures

Based on Blender's properties_texture.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_texture_settings(Panel):
    """Texture Settings"""
    bl_label = "Texture"
    bl_idname = "QPANEL_PT_texture_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'TEXTURE'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="Texture Slots:", icon='TEXTURE')
        col.label(text="(Use Shader Editor for modern workflow)")


class QPANEL_PT_texture_image(Panel):
    """Image Texture"""
    bl_label = "Image Texture"
    bl_idname = "QPANEL_PT_texture_image"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'TEXTURE'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="Image Textures:", icon='IMAGE_DATA')
        
        # List all images in blend file
        if bpy.data.images:
            box = layout.box()
            for img in bpy.data.images:
                row = box.row()
                row.label(text=img.name, icon='IMAGE')
                row.label(text=f"{img.size[0]}x{img.size[1]}" if img.size[0] > 0 else "No size")
        else:
            col.label(text="No images loaded")
        
        layout.separator()
        col = layout.column()
        col.operator("image.open", text="Open Image", icon='FILE_FOLDER')


class QPANEL_PT_texture_mapping(Panel):
    """Texture Mapping"""
    bl_label = "Mapping"
    bl_idname = "QPANEL_PT_texture_mapping"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'TEXTURE'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="Texture Coordinate Systems:", icon='ORIENTATION_VIEW')
        col.label(text="• Generated")
        col.label(text="• UV")
        col.label(text="• Object")
        col.label(text="• Camera")
        col.label(text="• Window")
        col.label(text="• Normal")


# Registration
classes = (
    QPANEL_PT_texture_settings,
    QPANEL_PT_texture_image,
    QPANEL_PT_texture_mapping,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
