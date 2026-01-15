# -*- coding: utf-8 -*-
"""
QPanel Assets - Particle System Properties
Particle systems, hair, and emitters

Based on Blender's properties_particle.py
"""

import bpy
from bpy.types import Panel


class QPANEL_PT_particle_system(Panel):
    """Particle System"""
    bl_label = "Particle System"
    bl_idname = "QPANEL_PT_particle_system"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PARTICLES'
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'
    
    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        
        if ob.particle_systems:
            psys = ob.particle_systems.active
            if psys:
                settings = psys.settings
                
                col = layout.column()
                col.prop(settings, "type", text="Type")
                
                col.separator()
                col.prop(settings, "count", text="Number")
                
                if settings.type == 'EMITTER':
                    col.prop(settings, "frame_start", text="Start")
                    col.prop(settings, "frame_end", text="End")
                    col.prop(settings, "lifetime", text="Lifetime")
        else:
            col = layout.column()
            col.operator("object.particle_system_add", text="Add Particle System", icon='PARTICLES')


class QPANEL_PT_particle_emission(Panel):
    """Particle Emission"""
    bl_label = "Emission"
    bl_idname = "QPANEL_PT_particle_emission"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PARTICLES'
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and 
                ob.particle_systems and 
                ob.particle_systems.active.settings.type == 'EMITTER')
    
    def draw(self, context):
        layout = self.layout
        psys = context.active_object.particle_systems.active
        settings = psys.settings
        
        col = layout.column()
        col.prop(settings, "emit_from", text="Emit From")
        col.prop(settings, "use_emit_random", text="Random Order")
        
        col.separator()
        col.prop(settings, "normal_factor", text="Normal")
        col.prop(settings, "tangent_factor", text="Tangent")


class QPANEL_PT_particle_velocity(Panel):
    """Particle Velocity"""
    bl_label = "Velocity"
    bl_idname = "QPANEL_PT_particle_velocity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PARTICLES'
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and 
                ob.particle_systems and 
                ob.particle_systems.active.settings.type == 'EMITTER')
    
    def draw(self, context):
        layout = self.layout
        psys = context.active_object.particle_systems.active
        settings = psys.settings
        
        col = layout.column()
        col.label(text="Initial Velocity:")
        col.prop(settings, "factor_random", text="Randomize")
        
        col.separator()
        col.label(text="Emitter Geometry:")
        col.prop(settings, "object_align_factor", text="Object Velocity", slider=True)


class QPANEL_PT_particle_render(Panel):
    """Particle Render Settings"""
    bl_label = "Render"
    bl_idname = "QPANEL_PT_particle_render"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'PARTICLES'
    
    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.type == 'MESH' and ob.particle_systems
    
    def draw(self, context):
        layout = self.layout
        psys = context.active_object.particle_systems.active
        settings = psys.settings
        
        col = layout.column()
        col.prop(settings, "render_type", text="Render As")
        
        if settings.render_type == 'OBJECT':
            col.prop(settings, "instance_object", text="Instance Object")
        elif settings.render_type == 'COLLECTION':
            col.prop(settings, "instance_collection", text="Instance Collection")


# Registration
classes = (
    QPANEL_PT_particle_system,
    QPANEL_PT_particle_emission,
    QPANEL_PT_particle_velocity,
    QPANEL_PT_particle_render,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
