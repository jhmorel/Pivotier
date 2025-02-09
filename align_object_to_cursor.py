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
    # bpy.ops.ed.undo_push(message="Align Objects to Cursor")
    
    for obj in objects:
        # Skip non-transformable objects
        if not hasattr(obj, "location") or not hasattr(obj, "rotation_euler"):
            continue
            
        # Apply transformation
        obj.location = cursor.location.copy()
        obj.rotation_euler = cursor.rotation_euler.copy()
    
    return None

class OBJECT_OT_align_to_cursor(bpy.types.Operator):
    """Align selected objects to 3D cursor"""
    bl_idname = "object.align_to_cursor"
    bl_label = "Align Objects to Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0
    
    def execute(self, context):
        error = align_object_to_cursor(set(context.selected_objects))
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

# Registration
classes = (
    OBJECT_OT_align_to_cursor,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
