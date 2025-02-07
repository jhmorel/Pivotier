import bpy
import mathutils
import math

def align_pivot_to_cursor():
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

class OBJECT_OT_align_pivot_to_cursor(bpy.types.Operator):
    bl_idname = "object.align_pivot_to_cursor"
    bl_label = "Align Pivot to 3D Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        align_pivot_to_cursor()
        return {'FINISHED'}

class OBJECT_OT_invert_pivot_z_axis(bpy.types.Operator):
    bl_idname = "object.invert_pivot_z_axis"
    bl_label = "Invert Pivot Z Axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        invert_pivot_z_axis()
        return {'FINISHED'}

class VIEW3D_PT_align_pivot_to_cursor_panel(bpy.types.Panel):
    bl_label = "Align Pivot to 3D Cursor"
    bl_idname = "VIEW3D_PT_align_pivot_to_cursor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivotier'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.align_pivot_to_cursor")
        layout.operator("object.invert_pivot_z_axis")

def register():
    bpy.utils.register_class(OBJECT_OT_align_pivot_to_cursor)
    bpy.utils.register_class(OBJECT_OT_invert_pivot_z_axis)
    bpy.utils.register_class(VIEW3D_PT_align_pivot_to_cursor_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_align_pivot_to_cursor)
    bpy.utils.unregister_class(OBJECT_OT_invert_pivot_z_axis)
    bpy.utils.unregister_class(VIEW3D_PT_align_pivot_to_cursor_panel)

if __name__ == "__main__":
    register()
