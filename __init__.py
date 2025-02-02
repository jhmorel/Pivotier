"""
Pivotier - A Blender addon for enhanced object alignment and pivot point management.

This addon provides tools to streamline 3D modeling workflow by offering various
alignment utilities for objects, cursor, and view management.

Author: Javier Hernández Morel
Colaborators: Eniel Rodríguez Machado
License: MIT
"""

bl_info = {
    "name": "Pivotier",
    "author": "Javier Hernández Morel",
    "version": (1, 0, 0),
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

# Configuration
ADDON_MODULES = [
    preferences,
    batch_operations,
    align_cursor_to_normal,
    align_object_to_cursor,
    set_pivot_to_base,
    set_pivot_to_cursor,
    align_view_to_cursor,
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
    prefs = get_preferences(bpy.context)
    if not prefs or not prefs.enable_keymaps:
        return

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
    for module in ADDON_MODULES:
        importlib.reload(module)
        module.register()
    
    register_keymaps()

def unregister() -> None:
    """Unregister all addon modules and their classes."""
    unregister_keymaps()
    
    for module in ADDON_MODULES:
        module.unregister()

if __name__ == "__main__":
    register()
