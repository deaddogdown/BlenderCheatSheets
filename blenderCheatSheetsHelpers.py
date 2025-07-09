# originToBottom.py
import bpy
from mathutils import Vector

def set_origin_to_bottom():
    obj = bpy.context.active_object
    if obj and obj.type == 'MESH':
        # Save current cursor position
        original_cursor_location = bpy.context.scene.cursor.location.copy()
        
        # Get the lowest Z coordinate in world space
        bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_z = min(corner.z for corner in bbox)
        
        # Calculate bottom center
        x_center = sum(corner.x for corner in bbox) / 8
        y_center = sum(corner.y for corner in bbox) / 8
        
        # Set cursor to bottom center and set origin
        bpy.context.scene.cursor.location = (x_center, y_center, min_z)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Restore original cursor position
        bpy.context.scene.cursor.location = original_cursor_location

def set_origin_to_global_zero():
    obj = bpy.context.active_object
    if obj:
        # Store the current cursor location
        original_cursor_location = bpy.context.scene.cursor.location.copy()
        
        # Move cursor to world origin and set origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        # Restore the original cursor location
        bpy.context.scene.cursor.location = original_cursor_location

class MESH_OT_origin_to_bottom(bpy.types.Operator):
    bl_idname = "mesh.origin_to_bottom"
    bl_label = "Origin to Bottom"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        set_origin_to_bottom()
        return {'FINISHED'}

class MESH_OT_origin_to_global_zero(bpy.types.Operator):
    bl_idname = "mesh.origin_to_global_zero"
    bl_label = "Origin to Global Zero"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        set_origin_to_global_zero()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MESH_OT_origin_to_bottom)
    bpy.utils.register_class(MESH_OT_origin_to_global_zero)

def unregister():
    bpy.utils.unregister_class(MESH_OT_origin_to_bottom)
    bpy.utils.unregister_class(MESH_OT_origin_to_global_zero)