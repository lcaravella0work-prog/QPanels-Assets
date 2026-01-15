# -*- coding: utf-8 -*-
"""
QPanel Assets - NLA Editor Panels
Non-linear animation, actions, and strips

Based on Blender's space_nla.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_nla_tracks(Panel):
    """NLA Tracks"""
    bl_label = "NLA Tracks"
    bl_idname = "QPANEL_PT_nla_tracks"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        obj = context.active_object
        if obj and obj.animation_data:
            col = layout.column()
            col.label(text="NLA Tracks:", icon='NLA')
            col.prop(obj.animation_data, "use_nla", text="Use NLA")
            
            if obj.animation_data.nla_tracks:
                box = layout.box()
                for track in obj.animation_data.nla_tracks:
                    row = box.row()
                    row.prop(track, "name", text="")
                    row.prop(track, "mute", text="", icon='CHECKBOX_DEHLT' if track.mute else 'CHECKBOX_HLT')
        else:
            layout.label(text="No animation data", icon='INFO')


class QPANEL_PT_nla_strips(Panel):
    """NLA Strip Tools"""
    bl_label = "Strip Tools"
    bl_idname = "QPANEL_PT_nla_strips"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Add Strip:", icon='NLA_PUSHDOWN')
        col.operator("nla.actionclip_add", text="Add Action Strip")
        col.operator("nla.transition_add", text="Add Transition")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("nla.duplicate", text="Duplicate")
        col.operator("nla.delete", text="Delete")


# Registration
classes = (
    QPANEL_PT_nla_tracks,
    QPANEL_PT_nla_strips,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
