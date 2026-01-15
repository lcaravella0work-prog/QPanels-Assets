# -*- coding: utf-8 -*-
"""
QPanel Assets - Outliner Panel
Complete scene outliner with collections and object hierarchy

Based on Blender's native space_outliner.py
Fully portable popup display
"""

import bpy
from bpy.types import Panel, Operator


class QPANEL_PT_outliner(Panel):
    """Complete Outliner - Collections & Objects"""
    bl_label = "Outliner"
    bl_idname = "QPANEL_PT_outliner"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_qpanel_category = 'OUTLINER'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Collections section
        col_box = layout.box()
        col_header = col_box.row()
        col_header.label(text="Collections", icon='OUTLINER_COLLECTION')
        
        self.draw_collection(col_box, scene.collection, context, level=0)
        
        layout.separator()
        
        # Objects section
        obj_box = layout.box()
        obj_header = obj_box.row()
        obj_header.label(text="Objects", icon='OBJECT_DATAMODE')
        
        top_level = [obj for obj in scene.objects if obj.parent is None]
        for obj in sorted(top_level, key=lambda x: x.name):
            self.draw_object(obj_box, obj, context, level=0)
    
    def draw_collection(self, layout, collection, context, level=0):
        """Draw collection hierarchy"""
        if level == 0:
            row = layout.row(align=True)
            row.label(text="Scene Collection", icon='SCENE_DATA')
            row.prop(collection, "hide_viewport", text="", emboss=False)
            row.prop(collection, "hide_render", text="", emboss=False)
        
        for child in collection.children:
            row = layout.row(align=True)
            
            for _ in range(level + 1):
                row.label(text="", icon='BLANK1')
            
            row.prop(child, "hide_viewport", text="", emboss=False,
                    icon='HIDE_OFF' if not child.hide_viewport else 'HIDE_ON')
            row.label(text=child.name, icon='OUTLINER_COLLECTION')
            row.prop(child, "hide_render", text="", emboss=False)
            
            if child.children:
                self.draw_collection(layout, child, context, level + 1)
    
    def draw_object(self, layout, obj, context, level=0):
        """Draw object with children"""
        row = layout.row(align=True)
        
        for _ in range(level):
            row.label(text="", icon='BLANK1')
        
        row.prop(obj, "hide_viewport", text="", emboss=False,
                icon='HIDE_OFF' if not obj.hide_viewport else 'HIDE_ON')
        
        icon_map = {
            'MESH': 'OUTLINER_OB_MESH', 'CURVE': 'OUTLINER_OB_CURVE',
            'SURFACE': 'OUTLINER_OB_SURFACE', 'META': 'OUTLINER_OB_META',
            'FONT': 'OUTLINER_OB_FONT', 'ARMATURE': 'OUTLINER_OB_ARMATURE',
            'LATTICE': 'OUTLINER_OB_LATTICE', 'EMPTY': 'OUTLINER_OB_EMPTY',
            'LIGHT': 'OUTLINER_OB_LIGHT', 'CAMERA': 'OUTLINER_OB_CAMERA',
            'SPEAKER': 'OUTLINER_OB_SPEAKER', 'CURVES': 'OUTLINER_OB_CURVES',
            'POINTCLOUD': 'OUTLINER_OB_POINTCLOUD', 'VOLUME': 'OUTLINER_OB_VOLUME',
            'GPENCIL': 'OUTLINER_OB_GREASEPENCIL',
        }
        icon = icon_map.get(obj.type, 'OBJECT_DATA')
        
        op = row.operator("object.select_pattern", text=obj.name, icon=icon, emboss=False)
        op.pattern = obj.name
        op.case_sensitive = True
        op.extend = False
        
        row.prop(obj, "hide_render", text="", emboss=False)
        
        for child in sorted(obj.children, key=lambda x: x.name):
            self.draw_object(layout, child, context, level + 1)


class QPANEL_OT_show_outliner(Operator):
    """Show Outliner popup"""
    bl_idname = "qpanel.show_outliner"
    bl_label = "Outliner"
    bl_options = {'REGISTER'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=500)
    
    def draw(self, context):
        panel = QPANEL_PT_outliner()
        panel.draw(context)
    
    def execute(self, context):
        return {'FINISHED'}


classes = (
    QPANEL_PT_outliner,
    QPANEL_OT_show_outliner,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
