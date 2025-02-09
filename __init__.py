"""
Pivotier - A Blender addon for enhanced object alignment and pivot point management.

This addon provides tools to streamline 3D modeling workflow by offering various
alignment utilities for objects, cursor, and view management.

Author: Javier Hernández Morel
Colaborator: Eniel Rodríguez Machado
License: SPDX-License-Identifier: GPL-3.0-or-later
"""

bl_info = {
    "name": "Pivotier",
    "author": "Javier Hernández Morel",
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Pivotier",
    "description": "Tools for enhanced object alignment and pivot point management",
    "warning": "",
    "doc_url": "https://github.com/jhmorel/Pivotier",
    "category": "Object",
}

import importlib
from typing import List, Set, Optional
import bpy

# Import sub-modules
from . import preferences
from . import batch_operations
from . import align_cursor_to_normal
from . import align_object_to_cursor
from . import set_pivot_to_base
from . import set_pivot_to_cursor
from . import align_view_to_cursor
from . import properties
from . import ui

# Reload modules
if "bpy" in locals():
    importlib.reload(preferences)
    importlib.reload(batch_operations)
    importlib.reload(align_cursor_to_normal)
    importlib.reload(align_object_to_cursor)
    importlib.reload(set_pivot_to_base)
    importlib.reload(set_pivot_to_cursor)
    importlib.reload(align_view_to_cursor)
    importlib.reload(properties)
    importlib.reload(ui)

# Configuration
ADDON_MODULES = [
    preferences,
    batch_operations,
    align_cursor_to_normal,
    align_object_to_cursor,
    set_pivot_to_base,
    set_pivot_to_cursor,
    align_view_to_cursor,
    properties,
    ui,
]

# Addon category name used across all panels
ADDON_CATEGORY = "Pivotier"

# Keymap configuration
addon_keymaps: List[bpy.types.KeyMap] = []

def get_preferences(context: bpy.types.Context) -> Optional[preferences.PivotierPreferences]:
    """Get addon preferences.
    
    Args:
        context: Current Blender context
        
    Returns:
        Addon preferences or None if addon is not found
    """
    addon_prefs = context.preferences.addons.get(__package__)
    if addon_prefs:
        return addon_prefs.preferences
    return None

def register_keymaps() -> None:
    """Register addon keymaps."""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        # Align Cursor to Normal
        km = kc.keymaps.new(name="Mesh", space_type='EMPTY')
        kmi = km.keymap_items.new(
            "mesh.align_cursor_to_normal",
            type='C',
            value='PRESS',
            alt=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))

        # Align Object to Cursor
        km = kc.keymaps.new(name="Object Mode", space_type='EMPTY')
        kmi = km.keymap_items.new(
            "object.align_object_to_cursor",
            type='A',
            value='PRESS',
            alt=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))

        # Set Pivot to Base
        km = kc.keymaps.new(name="Object Mode", space_type='EMPTY')
        kmi = km.keymap_items.new(
            "object.set_pivot_to_base",
            type='B',
            value='PRESS',
            alt=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))

        # Set Pivot to Cursor
        km = kc.keymaps.new(name="Object Mode", space_type='EMPTY')
        kmi = km.keymap_items.new(
            "object.set_pivot_to_cursor",
            type='P',
            value='PRESS',
            alt=True,
            shift=True
        )
        addon_keymaps.append((km, kmi))

def unregister_keymaps() -> None:
    """Unregister addon keymaps."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register() -> None:
    """Register all addon modules and their classes."""
    preferences.register()
    properties.register()  # Register properties first
    batch_operations.register()
    align_cursor_to_normal.register()
    align_object_to_cursor.register()
    set_pivot_to_base.register()
    set_pivot_to_cursor.register()
    align_view_to_cursor.register()
    ui.register()  # Register UI last
    register_keymaps()

def unregister() -> None:
    """Unregister all addon modules and their classes."""
    unregister_keymaps()
    ui.unregister()  # Unregister UI first
    align_view_to_cursor.unregister()
    set_pivot_to_cursor.unregister()
    set_pivot_to_base.unregister()
    align_object_to_cursor.unregister()
    align_cursor_to_normal.unregister()
    batch_operations.unregister()
    properties.unregister()
    preferences.unregister()

if __name__ == "__main__":
    register()
