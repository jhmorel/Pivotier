"""
Set Pivot to Base - Sets the pivot point to the base center of objects.

This module provides functionality to set the pivot point of one or more objects
to the center of their base (minimum Z in local space), with options to respect
or ignore object rotation.
"""

import bpy
import bmesh
import mathutils
from typing import Optional, List, Tuple

def get_base_center_world(obj: bpy.types.Object, ignore_rotation: bool = False, use_lowest_vertex: bool = False) -> mathutils.Vector:
    """Calculate the world position of the object's base center.
    
    Args:
        obj: The object to calculate base center for
        ignore_rotation: If True, calculate base as if current rotation was applied to mesh data
        use_lowest_vertex: If True, use lowest vertex instead of bounds
        
    Returns:
        World space position of the object's base center
    """
    if use_lowest_vertex and obj.type == 'MESH':
        # Find lowest vertex in world space
        lowest_z = float('inf')
        lowest_vertices = []
        
        # Get a BMesh to access vertices
        if obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
        else:
            bm = bmesh.new()
            bm.from_mesh(obj.data)
        
        try:
            # First pass: find the lowest Z value
            for vert in bm.verts:
                # Transform vertex to world space
                if ignore_rotation:
                    # Get the object's current world matrix and its components
                    loc, rot, scale = obj.matrix_world.decompose()
                    rot_matrix = rot.to_matrix().to_4x4()
                    scale_matrix = mathutils.Matrix.Diagonal(scale.to_4d())
                    apply_rotation_matrix = rot_matrix @ scale_matrix
                    vert_world = loc + (apply_rotation_matrix @ vert.co)
                else:
                    vert_world = obj.matrix_world @ vert.co
                
                if abs(vert_world.z - lowest_z) < 0.0001:  # Using small epsilon for float comparison
                    lowest_vertices.append(vert.co.copy())
                elif vert_world.z < lowest_z:
                    lowest_z = vert_world.z
                    lowest_vertices = [vert.co.copy()]
        finally:
            if obj.mode != 'EDIT':
                bm.free()
        
        if lowest_vertices:
            # Calculate average position of lowest vertices
            avg_pos = mathutils.Vector((0, 0, 0))
            for vertex in lowest_vertices:
                avg_pos += vertex
            avg_pos /= len(lowest_vertices)
            
            # Move the average position to world space
            if ignore_rotation:
                loc, rot, scale = obj.matrix_world.decompose()
                rot_matrix = rot.to_matrix().to_4x4()
                scale_matrix = mathutils.Matrix.Diagonal(scale.to_4d())
                apply_rotation_matrix = rot_matrix @ scale_matrix
                return loc + (apply_rotation_matrix @ avg_pos)
            else:
                return obj.matrix_world @ avg_pos

    # If not using lowest vertex or no vertex found, use bounds
    if ignore_rotation:
        # Get the object's current world matrix and its components
        loc, rot, scale = obj.matrix_world.decompose()
        rot_matrix = rot.to_matrix().to_4x4()
        scale_matrix = mathutils.Matrix.Diagonal(scale.to_4d())
        
        # Create matrix that represents what would happen if we applied the rotation
        apply_rotation_matrix = rot_matrix @ scale_matrix
        
        bbox_corners = [mathutils.Vector(corner) for corner in obj.bound_box]
        bbox_transformed = [apply_rotation_matrix @ v for v in bbox_corners]
        
        # Find the bounds in transformed space
        min_x = min(v.x for v in bbox_transformed)
        max_x = max(v.x for v in bbox_transformed)
        min_y = min(v.y for v in bbox_transformed)
        max_y = max(v.y for v in bbox_transformed)
        min_z = min(v.z for v in bbox_transformed)
        
        # Calculate the base center point
        center = mathutils.Vector((
            (min_x + max_x) / 2,  # Center in X
            (min_y + max_y) / 2,  # Center in Y
            min_z                 # Bottom in Z
        ))
        
        # Move the center to world space
        return loc + center
    else:
        # Use regular bounding box in world space
        bbox_corners_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        
        # Find the bounds in world space
        min_x = min(v.x for v in bbox_corners_world)
        max_x = max(v.x for v in bbox_corners_world)
        min_y = min(v.y for v in bbox_corners_world)
        max_y = max(v.y for v in bbox_corners_world)
        min_z = min(v.z for v in bbox_corners_world)
        
        # Return the base center point in world space
        return mathutils.Vector((
            (min_x + max_x) / 2,  # Center in X
            (min_y + max_y) / 2,  # Center in Y
            min_z                 # Bottom in Z
        ))

def set_pivot_to_base(context, ignore_rotation: bool = False, use_lowest_vertex: bool = False) -> Optional[str]:
    """Set the pivot point to the base center for each object.
    
    Args:
        context: The current context
        ignore_rotation: If True, calculate base as if current rotation was applied to mesh data
        use_lowest_vertex: If True, use lowest vertex instead of bounds
        
    Returns:
        Error message if operation fails, None otherwise
    """
    objects = context.selected_objects
    if not objects:
        return "No objects selected"
    
    # Store cursor location and selection states
    cursor = context.scene.cursor
    cursor_location = cursor.location.copy()
    cursor_rotation = cursor.rotation_euler.copy()
    
    # Store active object
    active_obj = context.view_layer.objects.active
    
    # Store selection states
    selection_states = {obj: obj.select_get() for obj in bpy.data.objects}
    
    try:
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Process each object independently
        for obj in objects:
            if obj.type != 'MESH':
                continue
                
            # Select only this object and make it active
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # Calculate and set new pivot
            cursor.location = get_base_center_world(obj, ignore_rotation, use_lowest_vertex)
            
            if ignore_rotation:
                # Reset cursor rotation when ignoring object rotation
                cursor.rotation_euler = mathutils.Euler((0, 0, 0))
            else:
                # Use object's rotation
                cursor.rotation_euler = obj.rotation_euler.copy()
            
            # Set origin to cursor position for this object only
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            # Deselect the object before moving to next
            obj.select_set(False)
    
    finally:
        # Restore cursor location and rotation
        cursor.location = cursor_location
        cursor.rotation_euler = cursor_rotation
        
        # Restore selection states
        for obj, was_selected in selection_states.items():
            obj.select_set(was_selected)
        
        # Restore active object
        if active_obj:
            context.view_layer.objects.active = active_obj
    
    return None

class OBJECT_OT_set_pivot_to_base(bpy.types.Operator):
    """Set pivot point to base of selected objects"""
    bl_idname = "object.set_pivot_to_base"
    bl_label = "Set Pivot to Base"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0
    
    def execute(self, context):
        wm = context.window_manager
        props = wm.pivotier.pivot_to_base
        error = set_pivot_to_base(context, props.ignore_rotation, props.use_lowest_vertex)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

# Registration
classes = (
    OBJECT_OT_set_pivot_to_base,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
