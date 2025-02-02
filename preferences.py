"""
Pivotier Preferences - Handles user preferences and customization options.

This module provides a preferences system for the Pivotier addon,
allowing users to customize default behaviors and keymaps.
"""

import bpy
from typing import Set
from bl_ui.utils import PresetPanel
from bl_operators.presets import AddPresetBase

class VIEW3D_MT_pivotier_presets(bpy.types.Menu):
    """Preset menu for Pivotier preferences"""
    bl_label = "Pivotier Presets"
    preset_subdir = "pivotier"
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset

class PIVOTIER_OT_add_preset(AddPresetBase, bpy.types.Operator):
    """Add or remove a preset for Pivotier preferences"""
    bl_idname = "pivotier.preset_add"
    bl_label = "Add Pivotier Preset"
    preset_menu = "VIEW3D_MT_pivotier_presets"
    preset_subdir = "pivotier"

    preset_defines = [
        "prefs = bpy.context.preferences.addons['Pivotier'].preferences"
    ]

    preset_values = [
        "prefs.use_auto_align",
        "prefs.align_to_active",
        "prefs.preserve_location",
        "prefs.coordinate_space"
    ]

class PivotierPreferences(bpy.types.AddonPreferences):
    """Preferences for the Pivotier addon"""
    bl_idname = "Pivotier"

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

    # Keymap preferences
    enable_keymaps: bpy.props.BoolProperty(
        name="Enable Custom Keymaps",
        description="Enable custom keyboard shortcuts",
        default=True
    )

    def draw(self, context):
        layout = self.layout

        # Preset menu
        row = layout.row(align=True)
        row.menu("VIEW3D_MT_pivotier_presets", text=bpy.types.VIEW3D_MT_pivotier_presets.bl_label)
        row.operator("pivotier.preset_add", text="", icon='ADD')
        row.operator("pivotier.preset_add", text="", icon='REMOVE').remove_active = True

        # General settings
        box = layout.box()
        box.label(text="General Settings:", icon='PREFERENCES')
        
        col = box.column()
        col.prop(self, "use_auto_align")
        col.prop(self, "align_to_active")
        col.prop(self, "preserve_location")
        col.prop(self, "coordinate_space")

        # Keymap settings
        box = layout.box()
        box.label(text="Keymap Settings:", icon='KEYINGSET')
        col = box.column()
        col.prop(self, "enable_keymaps")
        
        if self.enable_keymaps:
            col.label(text="Keyboard Shortcuts:", icon='INFO')
            col.label(text="• Align Cursor to Normal: Alt + Shift + C")
            col.label(text="• Align Object to Cursor: Alt + Shift + A")
            col.label(text="• Set Pivot to Base: Alt + Shift + B")
            col.label(text="• Set Pivot to Cursor: Alt + Shift + P")

# Registration
classes = (
    VIEW3D_MT_pivotier_presets,
    PIVOTIER_OT_add_preset,
    PivotierPreferences,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
