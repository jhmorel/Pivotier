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
    
    # Calculate position like Blender's Cursor to Selected
    if sel_faces:
        # For faces, use the median of all selected vertices
        verts = set()
        for face in sel_faces:
            verts.update(face.verts)
        location = sum((v.co for v in verts), mathutils.Vector()) / len(verts)
        
        # Calculate median normal from faces
        normal = mathutils.Vector((0, 0, 0))
        for face in sel_faces:
            normal += face.normal
        normal = normal.normalized()
        
        # Use the first face's edge for tangent reference
        tangent = (sel_faces[0].verts[1].co - sel_faces[0].verts[0].co).normalized()
        return normal, location, tangent
        
    elif sel_edges:
        # For edges, use the median of all selected vertices
        verts = set()
        for edge in sel_edges:
            verts.update(edge.verts)
        location = sum((v.co for v in verts), mathutils.Vector()) / len(verts)
        
        # Calculate median normal and tangent from edges
        normal = mathutils.Vector((0, 0, 0))
        tangent = mathutils.Vector((0, 0, 0))
        for edge in sel_edges:
            edge_normal = edge.verts[0].normal.lerp(edge.verts[1].normal, 0.5)
            normal += edge_normal
            edge_tangent = (edge.verts[1].co - edge.verts[0].co)
            tangent += edge_tangent
        
        normal = normal.normalized()
        tangent = tangent.normalized()
        return normal, location, tangent
        
    elif sel_verts:
        # For vertices, use direct median of selected vertices
        location = sum((v.co for v in sel_verts), mathutils.Vector()) / len(sel_verts)
        
        # Calculate median normal from vertices
        normal = mathutils.Vector((0, 0, 0))
        for vert in sel_verts:
            normal += vert.normal
        normal = normal.normalized()
        
        # Use the first vertex's edge for tangent reference
        vert = sel_verts[0]
        linked_edges = vert.link_edges
        tangent = ((linked_edges[0].verts[1].co - linked_edges[0].verts[0].co).normalized()
                  if linked_edges else mathutils.Vector((1, 0, 0)))
        return normal, location, tangent
    
    return None

def align_cursor_to_normal(context) -> Optional[str]:
    """Align 3D cursor to the normal of selected mesh elements.
    
    Returns:
        Error message string if operation fails, None otherwise
    """
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

class VIEW3D_OT_align_cursor_to_normal(bpy.types.Operator):
    """Align the 3D cursor to the normal of the selected face"""
    bl_idname = "view3d.align_cursor_to_normal"
    bl_label = "Align Cursor to Normal"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH' and
                context.active_object and
                context.active_object.type == 'MESH')
    
    def execute(self, context):
        error = align_cursor_to_normal(context)
        if error:
            self.report({'ERROR'}, error)
            return {'CANCELLED'}
        return {'FINISHED'}

# Registration
classes = (
    VIEW3D_OT_align_cursor_to_normal,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
