"""
Align Object to Cursor - Aligns selected objects to the 3D cursor.

This module provides functionality to align one or more selected objects
to the position and rotation of the 3D cursor.
"""

import bpy
from typing import Set, Optional

def align_object_to_cursor(objects: Set[bpy.types.Object]) -> Optional[str]:
    """Align selected objects to the 3D cursor's location and rotation.
    
    Args:
        objects: Set of objects to align
        
    Returns:
        Error message string if operation fails, None otherwise
    """
    if not objects:
        return "No objects selected"
        
    cursor = bpy.context.scene.cursor
    
    # Store initial states for undo
    bpy.ops.ed.undo_push(message="Align Objects to Cursor")
    
    for obj in objects:
        # Skip non-transformable objects
        if not hasattr(obj, "location") or not hasattr(obj, "rotation_euler"):
            continue
            
        # Apply transformation
        obj.location = cursor.location.copy()
        obj.rotation_euler = cursor.rotation_euler.copy()
    
    return None

class OBJECT_OT_align_object_to_cursor(bpy.types.Operator):
    """Align selected objects to the 3D cursor's position and rotation"""
    bl_idname = "object.align_object_to_cursor"
    bl_label = "Align Object to Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'
    
    def execute(self, context):
        error = align_object_to_cursor(set(context.selected_objects))
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

class VIEW3D_PT_align_object_to_cursor_panel(bpy.types.Panel):
    """Panel for Align Object to Cursor tool"""
    bl_label = "Align Object to Cursor"
    bl_idname = "VIEW3D_PT_align_object_to_cursor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivotier'
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        # Show selection info and operator
        if context.mode == 'OBJECT':
            if context.selected_objects:
                col.operator("object.align_object_to_cursor")
                col.label(text=f"Selected: {len(context.selected_objects)} objects")
            else:
                col.label(text="No objects selected", icon='ERROR')
        else:
            col.label(text="Enter Object Mode to use", icon='INFO')

# Registration
classes = (
    OBJECT_OT_align_object_to_cursor,
    VIEW3D_PT_align_object_to_cursor_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
