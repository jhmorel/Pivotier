"""
Set Pivot to Base - Sets the pivot point to the base center of objects.

This module provides functionality to set the pivot point of one or more objects
to the center of their base (minimum Z in local space), with options to respect
or ignore object rotation.
"""

import bpy
import mathutils
from typing import Optional, List, Tuple

class SetPivotToBaseProperties(bpy.types.PropertyGroup):
    """Properties for Set Pivot to Base operator"""
    ignore_rotation: bpy.props.BoolProperty(
        name="Treat As Default Orientation",
        description="Calculate base as if current rotation was the default orientation (without applying rotation)",
        default=False
    )

def get_base_center_world(obj: bpy.types.Object, ignore_rotation: bool = False) -> mathutils.Vector:
    """Calculate the world position of the object's base center.
    
    Args:
        obj: The object to calculate base center for
        ignore_rotation: If True, calculate base as if current rotation was applied to mesh data
        
    Returns:
        World space position of the object's base center
    """
    if ignore_rotation:
        # Get the object's current world matrix and its components
        loc, rot, scale = obj.matrix_world.decompose()
        rot_matrix = rot.to_matrix().to_4x4()
        scale_matrix = mathutils.Matrix.Diagonal(scale.to_4d())
        
        # Create matrix that represents what would happen if we applied the rotation
        # This is equivalent to Blender's "Apply Rotation" operation
        apply_rotation_matrix = rot_matrix @ scale_matrix
        
        # Transform bounding box corners as if rotation was applied
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
        # We only use location because we've already applied rotation and scale
        return loc + center
    else:
        # Get bounding box in local coordinates
        local_bbox = [mathutils.Vector(corner) for corner in obj.bound_box]
        
        # Find base coordinates (minimum Z)
        min_z = min(v.z for v in local_bbox)
        min_x = min(v.x for v in local_bbox)
        max_x = max(v.x for v in local_bbox)
        min_y = min(v.y for v in local_bbox)
        max_y = max(v.y for v in local_bbox)
        
        # Calculate base center in local space
        base_center_local = mathutils.Vector((
            (min_x + max_x) / 2,
            (min_y + max_y) / 2,
            min_z
        ))
        
        # Convert to world space using full transformation
        return obj.matrix_world @ base_center_local

def set_pivot_to_base(objects: List[bpy.types.Object], ignore_rotation: bool = False) -> Optional[str]:
    """Set the pivot point to the base center for each object.
    
    Args:
        objects: List of objects to process
        ignore_rotation: If True, calculate base as if objects had no rotation
        
    Returns:
        Error message if operation fails, None otherwise
    """
    if not objects:
        return "No objects selected"
    
    # Store cursor location and selection states
    cursor = bpy.context.scene.cursor
    cursor_location = cursor.location.copy()
    cursor_rotation = cursor.rotation_euler.copy()
    
    # Store active object
    active_obj = bpy.context.view_layer.objects.active
    
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
            bpy.context.view_layer.objects.active = obj
            
            # Calculate and set new pivot
            base_center = get_base_center_world(obj, ignore_rotation)
            cursor.location = base_center
            
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
            bpy.context.view_layer.objects.active = active_obj
    
    return None

class OBJECT_OT_set_pivot_to_base(bpy.types.Operator):
    """Set the pivot point to the base center of selected objects"""
    bl_idname = "object.set_pivot_to_base"
    bl_label = "Set Pivot to Base"
    bl_options = {'REGISTER', 'UNDO'}
    
    ignore_rotation: bpy.props.BoolProperty(
        name="Treat As Default Orientation",
        description="Calculate base as if current rotation was the default orientation (without applying rotation)",
        default=False
    )
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.selected_objects and
                any(obj.type == 'MESH' for obj in context.selected_objects))
    
    def invoke(self, context, event):
        self.ignore_rotation = context.scene.set_pivot_to_base_props.ignore_rotation
        return self.execute(context)
    
    def execute(self, context):
        error = set_pivot_to_base(context.selected_objects, self.ignore_rotation)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        
        # Update the scene property to match
        context.scene.set_pivot_to_base_props.ignore_rotation = self.ignore_rotation
        
        num_processed = sum(1 for obj in context.selected_objects if obj.type == 'MESH')
        self.report({'INFO'}, f"Set pivot to base for {num_processed} objects")
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "ignore_rotation")

class VIEW3D_PT_set_pivot_to_base_panel(bpy.types.Panel):
    """Panel for Set Pivot to Base tool"""
    bl_label = "Set Pivot to Base"
    bl_idname = "VIEW3D_PT_set_pivot_to_base_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align Toolkit'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.set_pivot_to_base_props
        
        if context.mode == 'OBJECT':
            # Count eligible objects
            mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
            num_selected = len(mesh_objects)
            
            if num_selected > 0:
                col = layout.column(align=True)
                col.prop(props, "ignore_rotation")
                op = col.operator("object.set_pivot_to_base")
                col.label(text=f"Selected: {num_selected} mesh objects")
            else:
                col = layout.column()
                col.label(text="Select mesh objects to use", icon='INFO')
        else:
            layout.label(text="Enter Object Mode to use", icon='INFO')

# Registration
classes = (
    SetPivotToBaseProperties,
    OBJECT_OT_set_pivot_to_base,
    VIEW3D_PT_set_pivot_to_base_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.set_pivot_to_base_props = bpy.props.PointerProperty(type=SetPivotToBaseProperties)

def unregister():
    del bpy.types.Scene.set_pivot_to_base_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
