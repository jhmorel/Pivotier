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

class BatchAlignmentSettings(bpy.types.PropertyGroup):
    """Settings for batch alignment operations"""
    
    # Alignment axes flags
    align_x: bpy.props.BoolProperty(
        name="X",
        description="Align along X axis",
        default=True
    )
    align_y: bpy.props.BoolProperty(
        name="Y",
        description="Align along Y axis",
        default=True
    )
    align_z: bpy.props.BoolProperty(
        name="Z",
        description="Align along Z axis",
        default=True
    )
    
    # Alignment options
    relative_to: bpy.props.EnumProperty(
        name="Relative To",
        description="Reference for alignment",
        items=[
            ('ACTIVE', "Active Object", "Use active object as reference"),
            ('CURSOR', "3D Cursor", "Use 3D cursor as reference"),
            ('WORLD', "World Origin", "Use world origin as reference"),
            ('AVERAGE', "Selection Average", "Use average of selected objects")
        ],
        default='ACTIVE'
    )
    
    align_mode: bpy.props.EnumProperty(
        name="Align Mode",
        description="How to align objects",
        items=[
            ('LOCATION', "Location", "Align object locations"),
            ('ROTATION', "Rotation", "Align object rotations"),
            ('BOTH', "Both", "Align both location and rotation")
        ],
        default='BOTH'
    )

def get_alignment_reference(context: bpy.types.Context, settings: BatchAlignmentSettings) -> Tuple[mathutils.Vector, mathutils.Euler]:
    """Get reference location and rotation for alignment.
    
    Args:
        context: Current Blender context
        settings: Batch alignment settings
        
    Returns:
        Tuple of (location, rotation) to use as reference
    """
    if settings.relative_to == 'ACTIVE':
        active = context.active_object
        return active.location.copy(), active.rotation_euler.copy()
    
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

def batch_align_objects(context: bpy.types.Context, settings: BatchAlignmentSettings) -> Optional[str]:
    """Perform batch alignment of selected objects.
    
    Args:
        context: Current Blender context
        settings: Batch alignment settings
        
    Returns:
        Error message if operation fails, None otherwise
    """
    if len(context.selected_objects) < 1:
        return "No objects selected"
        
    if settings.relative_to == 'ACTIVE' and not context.active_object:
        return "No active object selected"
    
    # Get reference location and rotation
    ref_loc, ref_rot = get_alignment_reference(context, settings)
    
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
        settings = context.scene.batch_align_settings
        error = batch_align_objects(context, settings)
        
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
            
        return {'FINISHED'}

class VIEW3D_PT_batch_align_panel(bpy.types.Panel):
    """Panel for batch alignment operations"""
    bl_label = "Batch Align"
    bl_idname = "VIEW3D_PT_batch_align_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Align Toolkit'
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.batch_align_settings
        
        # Alignment axes
        box = layout.box()
        box.label(text="Align Axes:")
        row = box.row(align=True)
        row.prop(settings, "align_x", toggle=True)
        row.prop(settings, "align_y", toggle=True)
        row.prop(settings, "align_z", toggle=True)
        
        # Alignment options
        col = layout.column(align=True)
        col.prop(settings, "relative_to")
        col.prop(settings, "align_mode")
        
        # Operation info
        box = layout.box()
        box.label(text="Selection Info:")
        col = box.column()
        col.label(text=f"Selected: {len(context.selected_objects)} objects")
        if settings.relative_to == 'ACTIVE':
            col.label(text="Active: " + (context.active_object.name if context.active_object else "None"),
                     icon='ERROR' if not context.active_object else 'OBJECT_DATA')
        
        # Operator
        layout.operator("object.batch_align")

# Registration
classes = (
    BatchAlignmentSettings,
    OBJECT_OT_batch_align,
    VIEW3D_PT_batch_align_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.batch_align_settings = bpy.props.PointerProperty(type=BatchAlignmentSettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.batch_align_settings
