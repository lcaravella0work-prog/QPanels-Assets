# -*- coding: utf-8 -*-
"""
QPanel Assets - Shader/Node Editor Panels
Node editing, materials, and shader tools

Based on Blender's space_node.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_node_tree(Panel):
    """Node Tree Info"""
    bl_label = "Node Tree"
    bl_idname = "QPANEL_PT_node_tree"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SHADER'
    
    def draw(self, context):
        layout = self.layout
        
        obj = context.active_object
        if obj and obj.active_material:
            mat = obj.active_material
            col = layout.column()
            col.label(text=f"Material: {mat.name}", icon='MATERIAL')
            col.prop(mat, "use_nodes")
        else:
            layout.label(text="No active material", icon='INFO')


class QPANEL_PT_shader_add(Panel):
    """Add Shader Nodes"""
    bl_label = "Add Shader"
    bl_idname = "QPANEL_PT_shader_add"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SHADER'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Shader Nodes:", icon='NODE_MATERIAL')
        col.operator("node.add_node", text="Principled BSDF").type = 'ShaderNodeBsdfPrincipled'
        col.operator("node.add_node", text="Diffuse BSDF").type = 'ShaderNodeBsdfDiffuse'
        col.operator("node.add_node", text="Glossy BSDF").type = 'ShaderNodeBsdfGlossy'
        col.operator("node.add_node", text="Emission").type = 'ShaderNodeEmission'
        col.operator("node.add_node", text="Mix Shader").type = 'ShaderNodeMixShader'
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Texture Nodes:", icon='TEXTURE')
        col.operator("node.add_node", text="Image Texture").type = 'ShaderNodeTexImage'
        col.operator("node.add_node", text="Noise Texture").type = 'ShaderNodeTexNoise'
        col.operator("node.add_node", text="Voronoi Texture").type = 'ShaderNodeTexVoronoi'
        col.operator("node.add_node", text="Wave Texture").type = 'ShaderNodeTexWave'


class QPANEL_PT_node_color(Panel):
    """Color/Vector Nodes"""
    bl_label = "Color & Vector"
    bl_idname = "QPANEL_PT_node_color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SHADER'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Color:", icon='COLOR')
        col.operator("node.add_node", text="RGB").type = 'ShaderNodeRGB'
        col.operator("node.add_node", text="ColorRamp").type = 'ShaderNodeValToRGB'
        col.operator("node.add_node", text="Mix RGB").type = 'ShaderNodeMixRGB'
        col.operator("node.add_node", text="Hue/Saturation").type = 'ShaderNodeHueSaturation'
        
        layout.separator()
        col = layout.column(align=True)
        col.label(text="Vector:", icon='DRIVER_ROTATIONAL_DIFFERENCE')
        col.operator("node.add_node", text="Mapping").type = 'ShaderNodeMapping'
        col.operator("node.add_node", text="Normal Map").type = 'ShaderNodeNormalMap'
        col.operator("node.add_node", text="Bump").type = 'ShaderNodeBump'
        col.operator("node.add_node", text="Vector Math").type = 'ShaderNodeVectorMath'


class QPANEL_PT_node_converter(Panel):
    """Converter Nodes"""
    bl_label = "Converters"
    bl_idname = "QPANEL_PT_node_converter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'SHADER'
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.label(text="Converters:", icon='ARROW_LEFTRIGHT')
        col.operator("node.add_node", text="Math").type = 'ShaderNodeMath'
        col.operator("node.add_node", text="Separate XYZ").type = 'ShaderNodeSeparateXYZ'
        col.operator("node.add_node", text="Combine XYZ").type = 'ShaderNodeCombineXYZ'
        col.operator("node.add_node", text="Separate RGB").type = 'ShaderNodeSeparateRGB'
        col.operator("node.add_node", text="Combine RGB").type = 'ShaderNodeCombineRGB'


# Registration
classes = (
    QPANEL_PT_node_tree,
    QPANEL_PT_shader_add,
    QPANEL_PT_node_color,
    QPANEL_PT_node_converter,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
