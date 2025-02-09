"""
UI - Unified user interface for the Pivotier addon.

This module provides a centralized UI panel that combines all Pivotier tools
in a single, organized interface following Blender's UI design patterns.
"""

import bpy
from . import (
    align_cursor_to_normal,
    align_object_to_cursor,
    align_view_to_cursor,
    batch_operations,
    set_pivot_to_base,
    set_pivot_to_cursor
)

class VIEW3D_PT_pivotier(bpy.types.Panel):
    """Main panel for Pivotier addon"""
    bl_label = "Pivotier"
    bl_idname = "VIEW3D_PT_pivotier"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivotier'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        # Batch Alignment Section
        box = layout.box()
        row = box.row()
        row.label(text="Batch Alignment", icon='OBJECT_DATA')
        
        settings = wm.pivotier.batch_align
        
        # Alignment axes
        col = box.column(align=True)
        col.label(text="Align Axes:")
        row = col.row(align=True)
        row.prop(settings, "align_x", toggle=True)
        row.prop(settings, "align_y", toggle=True)
        row.prop(settings, "align_z", toggle=True)
        
        # Alignment options
        col = box.column(align=True)
        col.prop(settings, "relative_to")
        col.prop(settings, "align_mode")
        
        # Operation info
        if context.mode == 'OBJECT':
            col = box.column()
            col.label(text=f"Selected: {len(context.selected_objects)} objects")
            if settings.relative_to == 'ACTIVE':
                col.label(text="Active: " + (context.active_object.name if context.active_object else "None"),
                         icon='ERROR' if not context.active_object else 'OBJECT_DATA')
            
            # Operator
            col.operator("object.batch_align")

        # Pivot Point Section
        box = layout.box()
        row = box.row()
        row.label(text="Pivot Point", icon='PIVOT_CURSOR')
        
        col = box.column(align=True)
        # Set Pivot to Base
        props = wm.pivotier.pivot_to_base
        col.label(text="Set Pivot to Base:")
        col.prop(props, "ignore_rotation")
        col.prop(props, "use_lowest_vertex")
        col.operator("object.set_pivot_to_base", icon='PIVOT_BOUNDBOX')
        
        # Set Pivot to Cursor
        col.separator()
        col.label(text="Set Pivot to Cursor:")
        col.operator("object.set_pivot_to_cursor", icon='PIVOT_CURSOR')
        
        # Invert Pivot Z Axis
        col.separator()
        col.operator("object.invert_pivot_z_axis", icon='ARROW_LEFTRIGHT')

        # Cursor Alignment Section
        box = layout.box()
        row = box.row()
        row.label(text="Cursor Alignment", icon='ORIENTATION_CURSOR')
        
        col = box.column(align=True)
        # Align Cursor to Normal
        col.operator("view3d.align_cursor_to_normal", icon='NORMALS_FACE')
        
        # Align Object to Cursor
        col.operator("object.align_to_cursor", icon='OBJECT_ORIGIN')
        
        # Align View to Cursor
        col.operator("view3d.align_view_to_cursor", icon='VIEW_PERSPECTIVE')

# Registration
classes = (
    VIEW3D_PT_pivotier,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
