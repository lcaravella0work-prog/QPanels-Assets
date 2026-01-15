# -*- coding: utf-8 -*-
"""
QPanel Assets - Dopesheet/Timeline Panels
Animation timeline, keyframes, and dopesheet

Based on Blender's space_dopesheet.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_dopesheet_filters(Panel):
    """Dopesheet Filters"""
    bl_label = "Dopesheet Filters"
    bl_idname = "QPANEL_PT_dopesheet_filters"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="Show:", icon='FILTER')
        col.prop(context.space_data.dopesheet if hasattr(context, 'space_data') and hasattr(context.space_data, 'dopesheet') else context.scene, "show_only_selected", text="Only Selected")
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Data Types:")
        col.prop(context.preferences.edit, "use_keyframe_insert_auto", text="Auto Keyframe")


class QPANEL_PT_keyframe_tools(Panel):
    """Keyframe Tools"""
    bl_label = "Keyframe Tools"
    bl_idname = "QPANEL_PT_keyframe_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Insert Keyframe:", icon='KEYINGSET')
        col.operator("anim.keyframe_insert", text="Location").type = 'Location'
        col.operator("anim.keyframe_insert", text="Rotation").type = 'Rotation'
        col.operator("anim.keyframe_insert", text="Scale").type = 'Scaling'
        col.operator("anim.keyframe_insert_menu", text="Insert All")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("anim.keyframe_delete", text="Delete Keyframe")
        col.operator("anim.keyframe_clear", text="Clear Keyframes")


class QPANEL_PT_timeline_playback(Panel):
    """Timeline Playback"""
    bl_label = "Playback"
    bl_idname = "QPANEL_PT_timeline_playback"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column(align=True)
        col.label(text="Timeline:", icon='TIME')
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")
        col.prop(scene, "frame_current", text="Current")
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Playback:")
        col.prop(scene, "use_preview_range", text="Preview Range")
        col.prop(scene.render, "fps", text="Frame Rate")


class QPANEL_PT_action_editor(Panel):
    """Action Editor"""
    bl_label = "Action Editor"
    bl_idname = "QPANEL_PT_action_editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        obj = context.active_object
        if obj and obj.animation_data:
            col = layout.column()
            col.label(text="Active Action:", icon='ACTION')
            col.prop(obj.animation_data, "action", text="")
            
            if obj.animation_data.action:
                col.separator()
                col.label(text=f"Frames: {obj.animation_data.action.frame_range[0]:.0f} - {obj.animation_data.action.frame_range[1]:.0f}")
        else:
            layout.label(text="No animation data", icon='INFO')


# Registration
classes = (
    QPANEL_PT_dopesheet_filters,
    QPANEL_PT_keyframe_tools,
    QPANEL_PT_timeline_playback,
    QPANEL_PT_action_editor,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
