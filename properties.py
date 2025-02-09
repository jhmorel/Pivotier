"""
Properties - Centralized property definitions for the Pivotier addon.

This module defines all property groups used across the addon, organized under
a single WindowManager property group to avoid cluttering the UI.
"""

import bpy
from typing import Set

class SetPivotToBaseProperties(bpy.types.PropertyGroup):
    """Properties for Set Pivot to Base operator"""
    ignore_rotation: bpy.props.BoolProperty(
        name="Ignore Object Rotation",
        description="Calculate base point as if the object had no rotation (useful for rotated objects)",
        default=False
    )
    use_lowest_vertex: bpy.props.BoolProperty(
        name="Use Lowest Vertex",
        description="Set pivot to the lowest vertex instead of bounding box center",
        default=False
    )

class BatchAlignmentProperties(bpy.types.PropertyGroup):
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

class PivotierProperties(bpy.types.PropertyGroup):
    """Main property group for all Pivotier addon properties"""
    pivot_to_base: bpy.props.PointerProperty(type=SetPivotToBaseProperties)
    batch_align: bpy.props.PointerProperty(type=BatchAlignmentProperties)

# Registration
classes = (
    SetPivotToBaseProperties,
    BatchAlignmentProperties,
    PivotierProperties
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Register on WindowManager instead of Scene
    bpy.types.WindowManager.pivotier = bpy.props.PointerProperty(type=PivotierProperties)

def unregister():
    # Remove from WindowManager
    del bpy.types.WindowManager.pivotier
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
