# -*- coding: utf-8 -*-
"""
QPanel Assets - Armature Data Properties
Armature, bones, and rigging settings

Based on Blender's properties_data_armature.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_armature_bones(Panel):
    """Armature Bones"""
    bl_label = "Armature Bones"
    bl_idname = "QPANEL_PT_armature_bones"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ARMATURE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'
    
    def draw(self, context):
        layout = self.layout
        arm = context.active_object.data
        
        col = layout.column()
        col.label(text=f"Bones: {len(arm.bones)}", icon='BONE_DATA')
        
        if context.active_bone:
            box = layout.box()
            box.label(text=f"Active: {context.active_bone.name}")


class QPANEL_PT_armature_display(Panel):
    """Armature Display Settings"""
    bl_label = "Viewport Display"
    bl_idname = "QPANEL_PT_armature_display"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ARMATURE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE'
    
    def draw(self, context):
        layout = self.layout
        arm = context.active_object.data
        
        col = layout.column()
        col.prop(arm, "display_type", text="Display As")
        col.prop(arm, "show_names", text="Names")
        col.prop(arm, "show_axes", text="Axes")
        col.prop(arm, "show_bone_custom_shapes", text="Shapes")


class QPANEL_PT_armature_pose(Panel):
    """Armature Pose Settings"""
    bl_label = "Pose Options"
    bl_idname = "QPANEL_PT_armature_pose"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ARMATURE'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'ARMATURE' and context.mode == 'POSE'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.operator("pose.select_all", text="Select All").action = 'SELECT'
        col.operator("pose.select_all", text="Deselect All").action = 'DESELECT'
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("pose.copy", text="Copy Pose")
        col.operator("pose.paste", text="Paste Pose")


# Registration
classes = (
    QPANEL_PT_armature_bones,
    QPANEL_PT_armature_display,
    QPANEL_PT_armature_pose,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
