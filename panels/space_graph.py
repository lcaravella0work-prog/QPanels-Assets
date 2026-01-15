# -*- coding: utf-8 -*-
"""
QPanel Assets - Graph Editor Panels
F-Curve editing and animation curves

Based on Blender's space_graph.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_graph_view(Panel):
    """Graph View Settings"""
    bl_label = "Graph View"
    bl_idname = "QPANEL_PT_graph_view"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="View Options:", icon='GRAPH')
        col.prop(context.space_data if hasattr(context, 'space_data') else context.scene, "show_cursor", text="Show Cursor")
        col.prop(context.space_data if hasattr(context, 'space_data') else context.scene, "show_sliders", text="Show Sliders")


class QPANEL_PT_fcurve_modifiers(Panel):
    """F-Curve Modifiers"""
    bl_label = "F-Curve Modifiers"
    bl_idname = "QPANEL_PT_fcurve_modifiers"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'ANIMATION'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Add Modifier:", icon='MODIFIER')
        col.operator("graph.fmodifier_add", text="Noise").type = 'NOISE'
        col.operator("graph.fmodifier_add", text="Cycles").type = 'CYCLES'
        col.operator("graph.fmodifier_add", text="Limits").type = 'LIMITS'
        col.operator("graph.fmodifier_add", text="Envelope").type = 'ENVELOPE'


class QPANEL_PT_graph_interpolation(Panel):
    """Interpolation Tools"""
    bl_label = "Interpolation"
    bl_idname = "QPANEL_PT_graph_interpolation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Keyframe Interpolation:", icon='IPO_BEZIER')
        col.operator("graph.interpolation_type", text="Constant").type = 'CONSTANT'
        col.operator("graph.interpolation_type", text="Linear").type = 'LINEAR'
        col.operator("graph.interpolation_type", text="Bezier").type = 'BEZIER'
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Handle Type:")
        col.operator("graph.handle_type", text="Auto").type = 'AUTO'
        col.operator("graph.handle_type", text="Vector").type = 'VECTOR'
        col.operator("graph.handle_type", text="Aligned").type = 'ALIGNED'


# Registration
classes = (
    QPANEL_PT_graph_view,
    QPANEL_PT_fcurve_modifiers,
    QPANEL_PT_graph_interpolation,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
