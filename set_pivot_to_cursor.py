"""
Set Pivot to Cursor - Provides functionality to set object pivot points to cursor.
"""

import bpy
import mathutils
import math
from typing import Optional

def align_pivot_to_cursor(selected_objects=None):
    if selected_objects is None:
        obj = bpy.context.active_object
    else:
        obj = selected_objects[0]
    
    if obj is None:
        print("No object selected")
        return
    
    # Guardar el modo original
    original_mode = obj.mode

    # Guardar la orientación de transformación actual
    original_orientation = bpy.context.scene.transform_orientation_slots[0].type

    # Activar modo opciones, transforms, affect only origins
    bpy.context.tool_settings.use_transform_data_origin = True

    # Cambiar la orientación de transformación a "CURSOR"
    bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'

    # Mover el pivote a la ubicación del cursor 3D
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # Alinear el objeto a la orientación del cursor
    bpy.ops.transform.transform(mode='ALIGN')

    # Restablecer la orientación de transformación original
    bpy.context.scene.transform_orientation_slots[0].type = original_orientation

    # Desactivar modo opciones, transforms, affect only origins
    bpy.context.tool_settings.use_transform_data_origin = False

    # Restaurar el modo original
    if original_mode == 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

def invert_pivot_z_axis():
    obj = bpy.context.active_object
    
    if obj is None:
        print("No object selected")
        return
    
    # Guardar el modo original
    original_mode = obj.mode

    # Guardar la orientación de transformación actual
    original_orientation = bpy.context.scene.transform_orientation_slots[0].type

    # Activar modo opciones, transforms, affect only origins
    bpy.context.tool_settings.use_transform_data_origin = True

    # Cambiar la orientación de transformación a "LOCAL"
    bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'

    # Rotar el pivote 180 grados en el eje X para invertir el eje Z
    bpy.ops.transform.rotate(value=math.pi, orient_axis='X', constraint_axis=(True, False, False))

    # Restablecer la orientación de transformación original
    bpy.context.scene.transform_orientation_slots[0].type = original_orientation

    # Desactivar modo opciones, transforms, affect only origins
    bpy.context.tool_settings.use_transform_data_origin = False

    # Restaurar el modo original
    if original_mode == 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')

def set_pivot_to_cursor(context) -> Optional[str]:
    """Set pivot point to 3D cursor for selected objects.
    
    Args:
        context: Current context
        
    Returns:
        Error message if operation fails, None otherwise
    """
    if not context.selected_objects:
        return "No objects selected"
    
    # Store cursor location and rotation
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
        
        # Process each object
        for obj in context.selected_objects:
            # Skip non-mesh objects
            if obj.type != 'MESH':
                continue
                
            # Select only this object and make it active
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            # Set pivot to cursor
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            
            # Deselect for next iteration
            obj.select_set(False)
            
    except Exception as e:
        return str(e)
        
    finally:
        # Restore selection states
        for obj, state in selection_states.items():
            obj.select_set(state)
        
        # Restore cursor location and rotation
        cursor.location = cursor_location
        cursor.rotation_euler = cursor_rotation
        
        # Restore active object
        if active_obj:
            bpy.context.view_layer.objects.active = active_obj
    
    return None

class OBJECT_OT_align_pivot_to_cursor(bpy.types.Operator):
    bl_idname = "object.align_pivot_to_cursor"
    bl_label = "Align Pivot to 3D Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        align_pivot_to_cursor()
        return {'FINISHED'}

class OBJECT_OT_invert_pivot_z_axis(bpy.types.Operator):
    """Invert the Z axis of the pivot point"""
    bl_idname = "object.invert_pivot_z_axis"
    bl_label = "Invert Pivot Z Axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0
    
    def execute(self, context):
        invert_pivot_z_axis()
        return {'FINISHED'}

class OBJECT_OT_set_pivot_to_cursor(bpy.types.Operator):
    """Set pivot point to 3D cursor"""
    bl_idname = "object.set_pivot_to_cursor"
    bl_label = "Set Pivot to Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 0
    
    def execute(self, context):
        align_pivot_to_cursor()  # La función ya maneja la selección internamente
        return {'FINISHED'}

classes = (
    OBJECT_OT_align_pivot_to_cursor,
    OBJECT_OT_invert_pivot_z_axis,
    OBJECT_OT_set_pivot_to_cursor,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
