# -*- coding: utf-8 -*-
"""
QPanel Assets - Mesh Data Properties
Mesh editing, geometry, and mesh tools

Based on Blender's properties_data_mesh.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_mesh_data(Panel):
    """Mesh Data Properties"""
    bl_label = "Mesh Data"
    bl_idname = "QPANEL_PT_mesh_data"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'MESH'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        mesh = context.active_object.data
        
        col = layout.column()
        col.label(text="Mesh Info:", icon='MESH_DATA')
        
        stats = col.column(align=True)
        stats.label(text=f"Vertices: {len(mesh.vertices)}")
        stats.label(text=f"Edges: {len(mesh.edges)}")
        stats.label(text=f"Faces: {len(mesh.polygons)}")


class QPANEL_PT_mesh_normals(Panel):
    """Mesh Normals"""
    bl_label = "Normals"
    bl_idname = "QPANEL_PT_mesh_normals"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'MESH'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        mesh = context.active_object.data
        
        col = layout.column()
        col.prop(mesh, "use_auto_smooth", text="Auto Smooth")
        if mesh.use_auto_smooth:
            col.prop(mesh, "auto_smooth_angle", text="Angle")
        
        layout.separator()
        col = layout.column(align=True)
        col.operator("mesh.normals_make_consistent", text="Recalculate Outside")
        col.operator("mesh.flip_normals", text="Flip")


class QPANEL_PT_mesh_vertex_groups(Panel):
    """Mesh Vertex Groups"""
    bl_label = "Vertex Groups"
    bl_idname = "QPANEL_PT_mesh_vertex_groups"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'MESH'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        row = layout.row()
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index")
        
        col = row.column(align=True)
        col.operator("object.vertex_group_add", icon='ADD', text="")
        col.operator("object.vertex_group_remove", icon='REMOVE', text="")


class QPANEL_PT_mesh_shape_keys(Panel):
    """Mesh Shape Keys"""
    bl_label = "Shape Keys"
    bl_idname = "QPANEL_PT_mesh_shape_keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'MESH'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        mesh = ob.data
        
        if mesh.shape_keys:
            row = layout.row()
            row.template_list("MESH_UL_shape_keys", "", mesh.shape_keys, "key_blocks", ob, "active_shape_key_index")
        else:
            col = layout.column()
            col.operator("object.shape_key_add", icon='ADD', text="Add Shape Key")


class QPANEL_PT_mesh_uv_maps(Panel):
    """Mesh UV Maps"""
    bl_label = "UV Maps"
    bl_idname = "QPANEL_PT_mesh_uv_maps"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'MESH'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        mesh = context.active_object.data
        
        row = layout.row()
        row.template_list("MESH_UL_uvmaps", "uvmaps", mesh, "uv_layers", mesh.uv_layers, "active_index")
        
        col = row.column(align=True)
        col.operator("mesh.uv_texture_add", icon='ADD', text="")
        col.operator("mesh.uv_texture_remove", icon='REMOVE', text="")


# Registration
classes = (
    QPANEL_PT_mesh_data,
    QPANEL_PT_mesh_normals,
    QPANEL_PT_mesh_vertex_groups,
    QPANEL_PT_mesh_shape_keys,
    QPANEL_PT_mesh_uv_maps,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
