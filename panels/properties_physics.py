# -*- coding: utf-8 -*-
"""
QPanel Assets - Physics Properties
Rigidbody, cloth, fluid, and physics simulation

Based on Blender's properties_physics_*.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_physics_rigidbody(Panel):
    """Rigid Body Physics"""
    bl_label = "Rigid Body"
    bl_idname = "QPANEL_PT_physics_rigidbody"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PHYSICS'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        if ob.rigid_body:
            rbo = ob.rigid_body
            col = layout.column()
            col.prop(rbo, "type", text="Type")
            
            col.separator()
            col.prop(rbo, "mass", text="Mass")
            col.prop(rbo, "friction", text="Friction")
            col.prop(rbo, "restitution", text="Bounciness")
        else:
            col = layout.column()
            col.operator("rigidbody.object_add", text="Add Rigid Body", icon='RIGID_BODY')


class QPANEL_PT_physics_cloth(Panel):
    """Cloth Physics"""
    bl_label = "Cloth"
    bl_idname = "QPANEL_PT_physics_cloth"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PHYSICS'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        # Find cloth modifier
        cloth_mod = None
        for mod in ob.modifiers:
            if mod.type == 'CLOTH':
                cloth_mod = mod
                break
        
        if cloth_mod:
            cloth = cloth_mod.settings
            col = layout.column()
            col.prop(cloth, "quality", text="Quality Steps")
            
            col.separator()
            col.label(text="Physical Properties:")
            col.prop(cloth, "mass", text="Mass")
            col.prop(cloth, "tension_stiffness", text="Tension")
            col.prop(cloth, "bending_stiffness", text="Bending")
        else:
            col = layout.column()
            col.operator("object.modifier_add", text="Add Cloth", icon='MOD_CLOTH').type = 'CLOTH'


class QPANEL_PT_physics_collision(Panel):
    """Collision Physics"""
    bl_label = "Collision"
    bl_idname = "QPANEL_PT_physics_collision"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PHYSICS'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        # Find collision modifier
        collision_mod = None
        for mod in ob.modifiers:
            if mod.type == 'COLLISION':
                collision_mod = mod
                break
        
        if collision_mod:
            coll = collision_mod.settings
            col = layout.column()
            col.prop(coll, "damping", text="Damping")
            col.prop(coll, "thickness_outer", text="Thickness")
            col.prop(coll, "friction_factor", text="Friction")
        else:
            col = layout.column()
            col.operator("object.modifier_add", text="Add Collision", icon='MOD_PHYSICS').type = 'COLLISION'


class QPANEL_PT_physics_fluid(Panel):
    """Fluid Physics"""
    bl_label = "Fluid"
    bl_idname = "QPANEL_PT_physics_fluid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PHYSICS'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        # Find fluid modifier
        fluid_mod = None
        for mod in ob.modifiers:
            if mod.type == 'FLUID':
                fluid_mod = mod
                break
        
        if fluid_mod:
            col = layout.column()
            col.prop(fluid_mod, "fluid_type", text="Type")
        else:
            col = layout.column()
            col.operator("object.modifier_add", text="Add Fluid", icon='MOD_FLUIDSIM').type = 'FLUID'


# Registration
classes = (
    QPANEL_PT_physics_rigidbody,
    QPANEL_PT_physics_cloth,
    QPANEL_PT_physics_collision,
    QPANEL_PT_physics_fluid,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
