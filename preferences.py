"""
Pivotier Preferences - Handles user preferences and customization options.

This module provides a preferences system for the Pivotier addon,
allowing users to customize default behaviors and keymaps.
"""

import bpy

class PivotierPreferences(bpy.types.AddonPreferences):
    """Preferences for the Pivotier addon"""
    bl_idname = __package__

    # General alignment preferences
    use_auto_align: bpy.props.BoolProperty(
        name="Auto-Align on Selection",
        description="Automatically align objects when selection changes",
        default=False
    )

    align_to_active: bpy.props.BoolProperty(
        name="Align to Active Object",
        description="Use active object as reference for alignment",
        default=True
    )

    preserve_location: bpy.props.BoolProperty(
        name="Preserve Original Location",
        description="Keep original object location when aligning rotation",
        default=False
    )

    coordinate_space: bpy.props.EnumProperty(
        name="Coordinate Space",
        description="Coordinate space for alignment operations",
        items=[
            ('GLOBAL', "Global Space", "Use global coordinate space"),
            ('LOCAL', "Local Space", "Use local coordinate space"),
            ('CURSOR', "Cursor Space", "Use 3D cursor space")
        ],
        default='GLOBAL'
    )

    def draw(self, context):
        layout = self.layout

        # General settings
        box = layout.box()
        box.label(text="General Settings:", icon='PREFERENCES')
        
        col = box.column()
        col.prop(self, "use_auto_align")
        col.prop(self, "align_to_active")
        col.prop(self, "preserve_location")
        col.prop(self, "coordinate_space")

# Registration
classes = (
    PivotierPreferences,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
