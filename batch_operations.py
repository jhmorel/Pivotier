"""
Batch Operations - Provides batch processing capabilities for alignment operations.

This module extends the basic alignment operations to support batch processing
with additional controls and options for multiple object operations.
"""

import bpy
import bmesh
import mathutils
from typing import Set, List, Dict, Optional, Tuple
from . import preferences

def get_alignment_reference(context: bpy.types.Context) -> Tuple[mathutils.Vector, mathutils.Euler]:
    """Get reference location and rotation for alignment.
    
    Args:
        context: Current Blender context
        
    Returns:
        Tuple of (location, rotation) to use as reference
    """
    wm = context.window_manager
    settings = wm.pivotier.batch_align
    
    if settings.relative_to == 'ACTIVE':
        if not context.active_object:
            return None
        return context.active_object.location.copy(), context.active_object.rotation_euler.copy()
    
    elif settings.relative_to == 'CURSOR':
        cursor = context.scene.cursor
        return cursor.location.copy(), cursor.rotation_euler.copy()
    
    elif settings.relative_to == 'WORLD':
        return mathutils.Vector((0, 0, 0)), mathutils.Euler((0, 0, 0))
    
    else:  # 'AVERAGE'
        loc = mathutils.Vector((0, 0, 0))
        rot = mathutils.Euler((0, 0, 0))
        count = 0
        
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                loc += obj.location
                rot.x += obj.rotation_euler.x
                rot.y += obj.rotation_euler.y
                rot.z += obj.rotation_euler.z
                count += 1
        
        if count > 0:
            loc /= count
            rot.x /= count
            rot.y /= count
            rot.z /= count
            
        return loc, rot

def batch_align_objects(context: bpy.types.Context) -> Optional[str]:
    """Perform batch alignment of selected objects.
    
    Args:
        context: Current Blender context
        
    Returns:
        Error message if operation fails, None otherwise
    """
    wm = context.window_manager
    settings = wm.pivotier.batch_align
    
    if len(context.selected_objects) < 1:
        return "No objects selected"
        
    if settings.relative_to == 'ACTIVE' and not context.active_object:
        return "No active object selected"
    
    # Get reference location and rotation
    reference = get_alignment_reference(context)
    if not reference:
        return "Could not determine alignment reference"
    
    ref_loc, ref_rot = reference
    
    # Store initial states for undo
    bpy.ops.ed.undo_push(message="Batch Align Objects")
    
    # Apply alignment to selected objects
    for obj in context.selected_objects:
        if obj == context.active_object and settings.relative_to == 'ACTIVE':
            continue
            
        if settings.align_mode in {'LOCATION', 'BOTH'}:
            if settings.align_x:
                obj.location.x = ref_loc.x
            if settings.align_y:
                obj.location.y = ref_loc.y
            if settings.align_z:
                obj.location.z = ref_loc.z
                
        if settings.align_mode in {'ROTATION', 'BOTH'}:
            if settings.align_x:
                obj.rotation_euler.x = ref_rot.x
            if settings.align_y:
                obj.rotation_euler.y = ref_rot.y
            if settings.align_z:
                obj.rotation_euler.z = ref_rot.z
    
    return None

class OBJECT_OT_batch_align(bpy.types.Operator):
    """Align multiple objects with advanced options"""
    bl_idname = "object.batch_align"
    bl_label = "Batch Align Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                len(context.selected_objects) > 0)
    
    def execute(self, context):
        error = batch_align_objects(context)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

# Registration
classes = (
    OBJECT_OT_batch_align,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
