"""
Align Cursor to Normal - Aligns the 3D cursor to face, edge, or vertex normals.

This module provides functionality to align the 3D cursor to the normal direction
of selected mesh elements in edit mode.
"""

import bpy
import bmesh
import mathutils
from typing import Optional, Tuple, List

def get_selection_data(bm: bmesh.types.BMesh) -> Tuple[List, List, List]:
    """Get lists of selected faces, edges, and vertices from the BMesh.
    
    Args:
        bm: BMesh object to analyze
        
    Returns:
        Tuple containing lists of selected faces, edges, and vertices
    """
    return ([f for f in bm.faces if f.select],
            [e for e in bm.edges if e.select],
            [v for v in bm.verts if v.select])

def compute_alignment_data(bm: bmesh.types.BMesh) -> Optional[Tuple[mathutils.Vector, mathutils.Vector, mathutils.Vector]]:
    """Compute normal, location and tangent vectors based on selection.
    
    Args:
        bm: BMesh object containing the selection
        
    Returns:
        Tuple of (normal, location, tangent) vectors or None if invalid selection
    """
    sel_faces, sel_edges, sel_verts = get_selection_data(bm)
    
    if sel_faces:
        face = sel_faces[0]
        normal = face.normal
        location = face.calc_center_median()
        tangent = (face.verts[1].co - face.verts[0].co).normalized()
        return normal, location, tangent
        
    elif sel_edges:
        edge = sel_edges[0]
        normal = edge.verts[0].normal.lerp(edge.verts[1].normal, 0.5).normalized()
        location = edge.verts[0].co.lerp(edge.verts[1].co, 0.5)
        tangent = (edge.verts[1].co - edge.verts[0].co).normalized()
        return normal, location, tangent
        
    elif sel_verts:
        vert = sel_verts[0]
        normal = vert.normal
        location = vert.co
        linked_edges = vert.link_edges
        tangent = ((linked_edges[0].verts[1].co - linked_edges[0].verts[0].co).normalized()
                  if linked_edges else mathutils.Vector((1, 0, 0)))
        return normal, location, tangent
    
    return None

def align_cursor_to_normal() -> Optional[str]:
    """Align 3D cursor to the normal of selected mesh elements.
    
    Returns:
        Error message string if operation fails, None otherwise
    """
    context = bpy.context
    if not context.edit_object:
        return "No object in edit mode"
        
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    
    alignment_data = compute_alignment_data(bm)
    if not alignment_data:
        return "No valid selection found"
        
    normal, location, tangent = alignment_data
    
    # Ensure tangent is not parallel to normal
    if abs(normal.dot(tangent)) > 0.99:
        tangent = mathutils.Vector((1, 0, 0))
        if abs(normal.dot(tangent)) > 0.99:
            tangent = mathutils.Vector((0, 1, 0))
    
    # Compute orientation matrix
    binormal = normal.cross(tangent).normalized()
    tangent = binormal.cross(normal).normalized()
    orientation_matrix = mathutils.Matrix((tangent, binormal, normal)).transposed().to_4x4()
    loc_matrix = mathutils.Matrix.Translation(location)
    transform_matrix = loc_matrix @ orientation_matrix
    
    # Apply transformation
    context.scene.cursor.matrix = obj.matrix_world @ transform_matrix
    return None

class MESH_OT_align_cursor_to_normal(bpy.types.Operator):
    """Align 3D cursor to the normal of selected mesh elements"""
    bl_idname = "mesh.align_cursor_to_normal"
    bl_label = "Align Cursor to Normal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.edit_object is not None
    
    def execute(self, context):
        error = align_cursor_to_normal()
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

class VIEW3D_PT_align_cursor_to_normal_panel(bpy.types.Panel):
    """Panel for Align Cursor to Normal tool"""
    bl_label = "Align Cursor to Normal"
    bl_idname = "VIEW3D_PT_align_cursor_to_normal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pivotier'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if context.edit_object:
            row.operator("mesh.align_cursor_to_normal")
        else:
            row.label(text="Enter Edit Mode to use", icon='INFO')

# Registration
classes = (
    MESH_OT_align_cursor_to_normal,
    VIEW3D_PT_align_cursor_to_normal_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
