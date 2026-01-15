# -*- coding: utf-8 -*-
"""
QPanel Assets - Video Sequencer Panels
Video editing, strips, and effects

Based on Blender's space_sequencer.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_sequencer_strips(Panel):
    """Sequencer Strip Tools"""
    bl_label = "Strip Tools"
    bl_idname = "QPANEL_PT_sequencer_strips"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SEQUENCER'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Add Strip:", icon='SEQUENCE')
        col.operator("sequencer.movie_strip_add", text="Movie", icon='FILE_MOVIE')
        col.operator("sequencer.image_strip_add", text="Image", icon='FILE_IMAGE')
        col.operator("sequencer.sound_strip_add", text="Sound", icon='FILE_SOUND')
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Edit:")
        col.operator("sequencer.split", text="Split")
        col.operator("sequencer.delete", text="Delete")
        col.operator("sequencer.duplicate_move", text="Duplicate")


class QPANEL_PT_sequencer_effects(Panel):
    """Sequencer Effects"""
    bl_label = "Effects"
    bl_idname = "QPANEL_PT_sequencer_effects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SEQUENCER'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Add Effect:", icon='SHADERFX')
        col.operator("sequencer.effect_strip_add", text="Cross").type = 'CROSS'
        col.operator("sequencer.effect_strip_add", text="Wipe").type = 'WIPE'
        col.operator("sequencer.effect_strip_add", text="Color Mix").type = 'COLORMIX'
        col.operator("sequencer.effect_strip_add", text="Transform").type = 'TRANSFORM'
        col.operator("sequencer.effect_strip_add", text="Glow").type = 'GLOW'


class QPANEL_PT_sequencer_preview(Panel):
    """Sequencer Preview Settings"""
    bl_label = "Preview"
    bl_idname = "QPANEL_PT_sequencer_preview"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SEQUENCER'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column()
        col.label(text="Playback:", icon='PLAY')
        col.prop(scene, "frame_current", text="Frame")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("screen.animation_play", text="Play", icon='PLAY')
        col.operator("screen.animation_cancel", text="Stop", icon='PAUSE')


# Registration
classes = (
    QPANEL_PT_sequencer_strips,
    QPANEL_PT_sequencer_effects,
    QPANEL_PT_sequencer_preview,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
