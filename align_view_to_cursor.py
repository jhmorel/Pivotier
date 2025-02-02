import bpy
import mathutils

# Función para alinear la vista al cursor 3D
def align_view_to_cursor():
    cursor_location = bpy.context.scene.cursor.location
    cursor_rotation = bpy.context.scene.cursor.rotation_euler

    # Calcular la ubicación de la vista
    view_direction = cursor_rotation.to_matrix() @ mathutils.Vector((0, 0, -1))
    view_location = cursor_location + view_direction

    # Ajustar la rotación para que el eje Z esté hacia arriba
    view_rotation = view_direction.to_track_quat('-Z', 'Y').to_matrix().to_4x4()
    view_rotation.translation = view_location

    # Establecer la vista para mirar hacia la ubicación del cursor
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    region_3d = area.spaces.active.region_3d

                    # Configurar la vista
                    region_3d.view_matrix = view_rotation.inverted()
                    region_3d.view_location = view_location

                    # Refrescar la vista
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    break
            break

class VIEW3D_OT_align_view_to_cursor(bpy.types.Operator):
    bl_idname = "view3d.align_view_to_cursor"
    bl_label = "Align View to Cursor"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        align_view_to_cursor()
        return {'FINISHED'}

class VIEW3D_PT_align_view_to_cursor_panel(bpy.types.Panel):
    bl_label = "Align View to Cursor"
    bl_idname = "VIEW3D_PT_align_view_to_cursor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivotier'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.align_view_to_cursor")

def register():
    bpy.utils.register_class(VIEW3D_OT_align_view_to_cursor)
    bpy.utils.register_class(VIEW3D_PT_align_view_to_cursor_panel)

def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_align_view_to_cursor)
    bpy.utils.unregister_class(VIEW3D_PT_align_view_to_cursor_panel)

if __name__ == "__main__":
    register()
