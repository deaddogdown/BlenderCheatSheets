import bpy
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from mathutils import Matrix, Vector



# Register collapsible section properties
def register_properties():
    props = [

        ('show_general', False),
        ('show_viewport', False),
        ('show_transform', False),
        ('show_cursor', False),
        ('show_world_origin', False),
        ('show_object_origin', False),
        ('show_primitives', False),
        ('show_object_mode', False),
        ('show_edit_mode', False),
        ('show_camera', False),        
        ('show_render', False),
        ('show_about', False),
        #
        #('shortcuts_show_help', False),
        ('show_help_general', False),
        ('show_help_viewport', False),
        ('show_help_transform', False),
        ('show_help_cursor', False),
        ('show_help_world_origin', False),
        ('show_help_object_origin', False),
        ('show_help_primitives', False),
        ('show_help_object_mode', False),
        ('show_help_edit_mode', False),
        ('show_help_camera', False),
        ('show_help_render', False),
        ('show_help_about', False),
    ]
    for prop_name, default in props:
        setattr(bpy.types.Scene, prop_name, bpy.props.BoolProperty(
            name=prop_name.replace('show_', '').title(),
            description=f"Toggle {prop_name.replace('show_', '').title()} section",
            default=default
        ))

def unregister_properties():
    props = [

        'show_general',
        'show_viewport',
        'show_transform',
        'show_cursor',
        'show_world_origin',
        'show_object_origin',
        'show_primitives',
        'show_object_mode',
        'show_edit_mode',
        'show_camera',        
        'show_render',
        'show_about'
        #
        #'shortcuts_show_help',
        'show_help_general',
        'show_help_viewport',
        'show_help_transform',
        'show_help_cursor',
        'show_help_world_origin',
        'show_help_object_origin',
        'show_help_primitives',
        'show_help_object_mode',
        'show_help_edit_mode',
        'show_help_camera',
        'show_help_render',
        'show_help_about',
    ]
    for prop in props:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)

def get_object_center(obj):
    """
    Returns the most accurate center of the object in world space.
    Prioritizes:
        1. Center of mass (if available)
        2. Bounding box center
        3. Average vertex position (fallback)
    """
    if obj.type != 'MESH':
        return None

    # 1. Try Center of Mass (requires physics calculation)
    try:
        bpy.ops.object.modifier_add(type='VERTEX_WEIGHT_PROXIMITY')  # Just to force a mass recalc
        bpy.ops.object.center_set(type='CENTER_OF_MASS')
        center_com = obj.matrix_world @ obj.location
        bpy.ops.object.modifier_remove(modifier="VertexWeightProximity")  # Cleanup
        return center_com
    except:
        pass  # Not all meshes can compute center of mass

    # 2. Use Bounding Box Center
    def bbox_center():
        corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        min_co = Vector((min(c[0] for c in corners),
                         min(c[1] for c in corners),
                         min(c[2] for c in corners)))
        max_co = Vector((max(c[0] for c in corners),
                         max(c[1] for c in corners),
                         max(c[2] for c in corners)))
        return (min_co + max_co) / 2

    # If object is not deformed or scaled oddly, use bounding box
    if obj.dimensions.length > 0:
        return bbox_center()

    # 3. Fallback: Average of vertex positions
    try:
        mesh = obj.data
        total = Vector()
        count = 0
        for v in mesh.vertices:
            total += obj.matrix_world @ v.co
            count += 1
        return total / count if count else None
    except:
        return None

def move_origin_point_to_cursor(direction='BOTTOM'):
    obj = bpy.context.active_object
    if not obj or obj.type != 'MESH':
        return False

    # Get bounding box corners in world space
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    if direction == 'BOTTOM':
        z_coord = min(corner.z for corner in bbox)
        x_center = sum(corner.x for corner in bbox) / 8
        y_center = sum(corner.y for corner in bbox) / 8
        origin_point = Vector((x_center, y_center, z_coord))
    elif direction == 'TOP':
        z_coord = max(corner.z for corner in bbox)
        x_center = sum(corner.x for corner in bbox) / 8
        y_center = sum(corner.y for corner in bbox) / 8
        origin_point = Vector((x_center, y_center, z_coord))
    elif direction == 'FRONT':
        y_coord = min(corner.y for corner in bbox)
        x_center = sum(corner.x for corner in bbox) / 8
        z_center = sum(corner.z for corner in bbox) / 8
        origin_point = Vector((x_center, y_coord, z_center))
    elif direction == 'BACK':
        y_coord = max(corner.y for corner in bbox)
        x_center = sum(corner.x for corner in bbox) / 8
        z_center = sum(corner.z for corner in bbox) / 8
        origin_point = Vector((x_center, y_coord, z_center))
    elif direction == 'LEFT':
        x_coord = min(corner.x for corner in bbox)
        y_center = sum(corner.y for corner in bbox) / 8
        z_center = sum(corner.z for corner in bbox) / 8
        origin_point = Vector((x_coord, y_center, z_center))
    elif direction == 'RIGHT':
        x_coord = max(corner.x for corner in bbox)
        y_center = sum(corner.y for corner in bbox) / 8
        z_center = sum(corner.z for corner in bbox) / 8
        origin_point = Vector((x_coord, y_center, z_center))
    else:
        return False

    cursor_loc = bpy.context.scene.cursor.location
    delta = cursor_loc - origin_point
    obj.location += delta

    return True


class MESH_OT_top_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.top_origin_to_cursor"
    bl_label = "Top Origin to 3D Cursor"
    bl_description = "Move object so its top origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='TOP')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class MESH_OT_bottom_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.bottom_origin_to_cursor"
    bl_label = "Bottom Origin to 3D Cursor"
    bl_description = "Move object so its bottom origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='BOTTOM')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class MESH_OT_front_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.front_origin_to_cursor"
    bl_label = "Front Origin to 3D Cursor"
    bl_description = "Move object so its front origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='FRONT')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class MESH_OT_back_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.back_origin_to_cursor"
    bl_label = "Back Origin to 3D Cursor"
    bl_description = "Move object so its back origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='BACK')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class MESH_OT_left_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.left_origin_to_cursor"
    bl_label = "Left Origin to 3D Cursor"
    bl_description = "Move object so its left origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='LEFT')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class MESH_OT_right_origin_to_cursor(bpy.types.Operator):
    bl_idname = "mesh.right_origin_to_cursor"
    bl_label = "Right Origin to 3D Cursor"
    bl_description = "Move object so its right origin lands exactly on the 3D cursor"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        success = move_origin_point_to_cursor(direction='RIGHT')
        if not success:
            self.report({'WARNING'}, "Operation failed")
            return {'CANCELLED'}
        return {'FINISHED'}

class SHORTCUTS_OT_CursorToGeometryCenter(bpy.types.Operator):
    bl_idname = "shortcuts.cursor_to_geometry_center"
    bl_label = "3D Cursor to Geometry Center"
    bl_description = "Move 3D cursor to the center of the selected object's geometry (accurate, even if origin is offset)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.select_get():
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}

        center = get_object_center(obj)
        if not center:
            self.report({'WARNING'}, "Could not compute geometry center")
            return {'CANCELLED'}

        # Move 3D cursor to calculated center
        context.scene.cursor.location = center

        return {'FINISHED'}

class SHORTCUTS_OT_ObjectGeometryToCursor(bpy.types.Operator):
    bl_idname = "shortcuts.object_geometry_to_cursor"
    bl_label = "Object Geometry to 3D Cursor"
    bl_description = "Move object's geometry so its center aligns with the 3D cursor, without moving the origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.select_get():
            self.report({'WARNING'}, "No active object selected")
            return {'CANCELLED'}
        
        if obj.type != 'MESH':
            self.report({'INFO'}, "Only works on mesh objects")
            return {'CANCELLED'}

        geo_center = get_object_center(obj)
        cursor_loc = context.scene.cursor.location

        if not geo_center:
            self.report({'WARNING'}, "Could not compute object center")
            return {'CANCELLED'}

        delta = cursor_loc - geo_center

        mesh = obj.data
        mesh.transform(Matrix.Translation(delta))

        return {'FINISHED'}

# Optional: Add a custom operator to quickly set common unit combinations
class SHORTCUTS_OT_SetUnits(bpy.types.Operator):
    """Set units to common combinations"""
    bl_idname = "shortcuts.set_units"
    bl_label = "Set Units"
    bl_options = {'REGISTER', 'UNDO'}
    
    unit_preset: EnumProperty(
        name="Unit Preset",
        description="Choose a common unit setup",
        items=[
            ('DEFAULT', "Default (None)", "Blender's default units"),
            ('METRIC_M', "Metric - Meters", "Metric system with meters"),
            ('METRIC_CM', "Metric - Centimeters", "Metric system with centimeters"),
            ('IMPERIAL_FT', "Imperial - Feet", "Imperial system with feet"),
            ('IMPERIAL_IN', "Imperial - Inches", "Imperial system with inches"),
        ]
    )
    
    def execute(self, context):
        scene = context.scene
        
        if self.unit_preset == 'DEFAULT':
            scene.unit_system = 'NONE'
        elif self.unit_preset == 'METRIC_M':
            scene.unit_system = 'METRIC'
            scene.unit_length = 'METERS'
        elif self.unit_preset == 'METRIC_CM':
            scene.unit_system = 'METRIC'
            scene.unit_length = 'CENTIMETERS'
        elif self.unit_preset == 'IMPERIAL_FT':
            scene.unit_system = 'IMPERIAL'
            scene.unit_length = 'FEET'
        elif self.unit_preset == 'IMPERIAL_IN':
            scene.unit_system = 'IMPERIAL'
            scene.unit_length = 'INCHES'
        
        return {'FINISHED'}

class OBJECT_OT_reset_transforms(bpy.types.Operator):
    bl_idname = "object.reset_transforms"
    bl_label = "Reset Rotation & Scale"
    bl_description = "Clear rotation and scale of selected objects"

    def execute(self, context):
        # Clear rotation
        bpy.ops.object.rotation_clear(clear_delta=False)
        # Clear scale
        bpy.ops.object.scale_clear(clear_delta=False)
        return {'FINISHED'}

# The operator class
class MESH_OT_smart_snap(bpy.types.Operator):
    bl_idname = "mesh.smart_snap"
    bl_label = "Smart Snap"
    bl_description = "Set snap to: Vertex, Closest, Include Active, Move"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        ts = context.tool_settings
        
        # Enable snapping
        ts.use_snap = True
        
        # Set to Vertex
        ts.snap_elements = {'VERTEX'}
        
        # Set to Closest
        ts.snap_target = 'CLOSEST'
        
        # Reset all snap options to known defaults
        ts.use_snap_self = True                     # "Include Active" (prevents hunting other selected vertices)
        ts.use_snap_align_rotation = False          # "Align rotation to target"
        ts.use_snap_backface_culling = False        # "Backface culling"
        ts.use_snap_edit = True                     # "Include edited" 
        ts.use_snap_nonedit = False                 # "Include non-edited"
        ts.use_snap_selectable = False              # "Exclude non-selectable"
        ts.use_snap_rotate = False                  # "Rotate"
        ts.use_snap_scale = False                   # "Scale"
        
        return {'FINISHED'}

# The operator functions would need to be defined elsewhere in your addon:
class MESH_OT_smart_snap_vertex(bpy.types.Operator):
    bl_idname = "mesh.smart_snap_vertex"
    bl_label = "Smart Snap to Vertex"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Toggle: if already in vertex snap mode, turn off snapping
        if (context.tool_settings.use_snap and 
            context.tool_settings.snap_elements == {'VERTEX'}):
            context.tool_settings.use_snap = False
        else:
            # Enable snapping and set to vertex mode
            context.tool_settings.use_snap = True
            context.tool_settings.snap_elements = {'VERTEX'}
            context.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}

class MESH_OT_smart_snap_edge(bpy.types.Operator):
    bl_idname = "mesh.smart_snap_edge"
    bl_label = "Smart Snap to Edge Mid"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Toggle: if already in edge midpoint snap mode, turn off snapping
        if (context.tool_settings.use_snap and 
            context.tool_settings.snap_elements == {'EDGE_MIDPOINT'}):
            context.tool_settings.use_snap = False
        else:
            # Enable snapping and set to edge midpoint mode
            context.tool_settings.use_snap = True
            context.tool_settings.snap_elements = {'EDGE_MIDPOINT'}
            context.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}

class MESH_OT_smart_snap_face(bpy.types.Operator):
    bl_idname = "mesh.smart_snap_face"
    bl_label = "Smart Snap to Face Center"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Toggle: if already in face snap mode, turn off snapping
        if (context.tool_settings.use_snap and 
            context.tool_settings.snap_elements == {'FACE'}):
            context.tool_settings.use_snap = False
        else:
            # Enable snapping and set to face center mode
            context.tool_settings.use_snap = True
            context.tool_settings.snap_elements = {'FACE'}
            context.tool_settings.snap_target = 'CENTER'
        return {'FINISHED'}

        
class SHORTCUTS_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CheatSheets"
    bl_label = "CheatSheets"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        #layout.label(text=f"Help Enabled: {scene.shortcuts_show_help}")
        # Help toggle at top
        #row = layout.row()
        #row.scale_y = 1.2
        #if scene.shortcuts_show_help:
            #row.prop(scene, "shortcuts_show_help", text="BEGINNER USER", icon='HIDE_ON')
        #else:
            #row.prop(scene, "shortcuts_show_help", text="ADVANCED USER", icon='HELP')

        # Mode switch buttons at the top with visual feedback
        row = layout.row()
        row.scale_y = 1.5
        obj = context.object
        current_mode = obj.mode if obj else 'OBJECT'
        
        # Object Mode button
        sub_row = row.row()
        if current_mode == 'OBJECT':
            sub_row.alert = True
        sub_row.operator("object.switch_to_object_mode", text="Object Mode", icon='OBJECT_DATAMODE')
        
        # Edit Mode button
        sub_row = row.row()
        if current_mode == 'EDIT':
            sub_row.alert = True
        sub_row.operator("object.switch_to_edit_mode", text="Edit Mode", icon='EDITMODE_HLT')
        
        
        #if scene.shortcuts_show_help:
            #layout.separator()
            #layout.label(text="Common Commands:")    

        # 🧩 General
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_general", text="GENERAL", emboss=False, icon='INFO')
        
        # Help toggle specific to this section
        #if scene.shortcuts_show_help:
        row.prop(scene, "show_help_general", text="", icon='HELP' if scene.show_help_general else 'HIDE_ON', toggle=True)


        if scene.show_general:
            col = box.column(align=True)
        
            # Units Selection Section
            if scene.show_help_general:
                col.label(text="UNITS: Choose your measurement system")
            
            # Units dropdown - accessing the unit settings properly
            row = col.row()
            row.prop(scene.unit_settings, "system", text="Unit System")
            
            # Show length unit when metric or imperial is selected
            if scene.unit_settings.system in {'METRIC', 'IMPERIAL'}:
                row = col.row()
                row.prop(scene.unit_settings, "length_unit", text="Length Unit")
            
            # Newbie-friendly descriptions
            #layout.separator()
            if scene.show_help_general:
                col.label(text="Unit Guide:")
                if scene.unit_settings.system == 'NONE':
                    col.label(text="• None: Uses Blender's default units")
                    col.label(text="• Good for beginners learning basics")
                elif scene.unit_settings.system == 'METRIC':
                    col.label(text="• Metric: Meters, centimeters, etc.")
                    col.label(text="• Global measurement system for precise work")
                elif scene.unit_settings.system == 'IMPERIAL':
                    col.label(text="• Imperial: Feet, inches, etc.")
                    col.label(text="• Common in USA architecture/design")
            
            
            col.separator()
            col.separator()
        
            
            col.label(text="Useful Commands:")    
            row = col.row()
            row.scale_y = 1.35
            row.operator("wm.search_menu", text="Search Operators: F3 or Spacebar")
            
            
            # Info labels for shortcuts that don't need operators:
            col.separator()
            if scene.show_help_general:
                col.label(text="Keyboard Shortcuts:")
                col.label(text="• Undo: Ctrl + Z")
                col.label(text="• Redo: Ctrl + Shift + Z")
                col.label(text="• Copy: Ctrl + C")
                col.label(text="• Paste: Ctrl + V")
            
            col.separator()
            col.separator()
            
            
        
        # 🧩 Viewport
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_viewport", text="VIEWPORT", emboss=False, icon='VIEW_CAMERA')
        
        row.prop(scene, "show_help_viewport", text="", icon='HELP' if scene.show_help_viewport else 'HIDE_ON', toggle=True)
        
        if scene.show_viewport:
            col = box.column(align=True)
            
            
            col.separator()
            # ADVANCED NAVIGATION
            col.label(text="Advanced Navigation:")
            row = col.row()
            row.scale_y = 1.35
            # Transform Orientation buttons with visual feedback
            row.operator("view3d.walk", text="Walk Mode (Shift + `)")
            
            col.separator()
            col.label(text="Global/Local:")
            # Transform Orientation buttons with visual feedback

            row = col.row()
            # Transform Orientation buttons with visual feedback
            row.scale_y = 1.0
            current_orientation = context.scene.transform_orientation_slots[0].type

            # Global Orientation button
            sub_row = row.row()
            if current_orientation == 'GLOBAL':
                sub_row.alert = True
            op = sub_row.operator("wm.context_set_enum", text="Global", icon='ORIENTATION_GLOBAL')
            op.data_path = "scene.transform_orientation_slots[0].type"
            op.value = 'GLOBAL'

            # Local Orientation button
            sub_row = row.row()
            if current_orientation == 'LOCAL':
                sub_row.alert = True
            op = sub_row.operator("wm.context_set_enum", text="Local", icon='ORIENTATION_LOCAL')
            op.data_path = "scene.transform_orientation_slots[0].type"
            op.value = 'LOCAL'
            
            # VIEWPORT SETTINGS (Less common but useful)
            col.separator()
            col.separator()
            col.label(text="Viewport Settings:")
            if hasattr(context.preferences.inputs, 'use_mouse_emulate_3_button'):
                col.prop(context.preferences.inputs, "use_mouse_emulate_3_button", text="Emulate 3 Button Mouse")
            col.prop(context.preferences.view, "smooth_view", text="Smooth View Transitions")
            
            # THE WHY - What is the Viewport?
            if scene.show_help_viewport:
                col.label(text="Viewport = Your 3D Window")
                col.label(text="Navigate (move yourself) vs Transform (move objects)")
                col.separator()
                
                # MOUSE NAVIGATION (Most Important - Put First)
                col.label(text="Mouse Navigation:")
                col.label(text="• Orbit: Middle Mouse Button (MMB) Drag")
                col.label(text="• Pan: Shift + MMB Drag") 
                col.label(text="• Zoom: Scroll Wheel or Ctrl + MMB Drag")
            
            col.separator()
            col.separator()
            # QUICK NAVIGATION (High frequency)
            col.label(text="Quick Navigation:")
            col.operator("view3d.view_all", text="Frame All Objects (Home)")
            col.operator("view3d.view_selected", text="Frame Selected (Numpad .)")
            col.operator("view3d.snap_cursor_to_center", text="Reset View Focus (Shift + C)")
            col.operator("wm.context_toggle", text="Wireframe Overlay Toggle", icon='SHADING_WIRE').data_path = "space_data.overlay.show_wireframes"
            col.operator("wm.context_toggle", text="X-Ray Mode Toggle (Edit mode)", icon='XRAY').data_path = "space_data.shading.show_xray"
            
            
            col.separator()
            col.separator()
            # STANDARD VIEWS (For precision work)
            col.label(text="Standard Views (Numpad):")
            row = col.row(align=True)
            row.operator("view3d.view_axis", text="Top (7)").type = 'TOP'
            row.operator("view3d.view_axis", text="Front (1)").type = 'FRONT'
            row.operator("view3d.view_axis", text="Right (3)").type = 'RIGHT'
            row = col.row(align=True)
            row.operator("view3d.view_axis", text="Bottom (Ctrl + 7)").type = 'BOTTOM'
            row.operator("view3d.view_axis", text="Back (Ctrl + 1)").type = 'BACK'
            row.operator("view3d.view_axis", text="Left (Ctrl + 3)").type = 'LEFT'
            
            col.operator("view3d.view_persportho", text="Perspective/Orthographic (5)")
            
            
            
            col.separator()
            col.separator()
            # CAMERA OPERATIONS
            col.label(text="Camera:")
            col.operator("view3d.view_camera", text="Toggle Camera View (Numpad 0)")
            if context.scene.camera:
                col.operator("view3d.camera_to_view_selected", text="Align Camera to View (Ctrl + Alt + Numpad 0)")
                row = col.row()
                row.prop(context.space_data, "lock_camera", text="Lock Camera to View")
            else:
                col.label(text="No active camera in scene")
            
            col.separator()
            col.separator()


        # 🧩 Transform
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_transform", text="TRANSFORM", emboss=False, icon='ORIENTATION_GIMBAL')
        
        row.prop(scene, "show_help_transform", text="", icon='HELP' if scene.show_help_transform else 'HIDE_ON', toggle=True)
        
        if scene.show_transform:
            col = box.column(align=True)
            
            # THE WHY - What is Transform?
            if scene.show_help_transform:
                col.label(text="Transform = Change Position, Rotation, Scale")
                col.label(text="Works in: Object Mode & Edit Mode")
                col.separator()
            
            # CORE TRANSFORMS (work everywhere)
            col.label(text="Basic Transforms:")
            row = col.row()
            row.scale_y = 1.35
            row.operator("transform.translate", text="Move (G)")
            row.operator("transform.rotate", text="Rotate (R)")
            row.operator("transform.resize", text="Scale (S)")
            
            # CONSTRAINT HELPERS
            if scene.show_help_transform:
                col.label(text="Axis Constraints (after G/R/S):")
                col.label(text="• X-axis only: X • Y-axis only: Y • Z-axis only: Z")
                col.label(text="• Local axes: XX, YY, ZZ")
                
            col.separator()  
            # ADVANCED HELPERS
            col.label(text="Enable Snapping:")
            col.prop(context.tool_settings, "use_snap", text="Enable Snapping (SHIFT + TAB)") 
            # Smart Snaps section
 
            col.separator()
            col.label(text="Smart Snaps:")
            col.operator("mesh.smart_snap", text="Smart Snap", icon='SNAP_VERTEX')
            col.label(text="• Recommended default snap settings:")
            col.separator()
            col.operator("mesh.smart_snap_vertex", text="Smart Snap to Vertex", icon='VERTEXSEL')
            col.operator("mesh.smart_snap_edge", text="Smart Snap to Edge Mid", icon='EDGESEL') 
            col.operator("mesh.smart_snap_face", text="Smart Snap to Face Center", icon='FACESEL')
            
            col.separator()
            col.label(text="Proportional Editing:")
            col.operator("wm.context_toggle", text="Toggle Proportional Editing (O)", icon='PROP_ON').data_path = "tool_settings.use_proportional_edit_objects"
            
            col.separator()
            col.separator()
            
            
        # 🧩 3D Cursor
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_cursor", text="3D CURSOR", emboss=False, icon='CURSOR')
        
        row.prop(scene, "show_help_cursor", text="", icon='HELP' if scene.show_help_cursor else 'HIDE_ON', toggle=True)
        
        if scene.show_cursor:
            col = box.column(align=True)
            
            # Selection status button
            status_row = col.row()
            if context.selected_objects:
                status_row.alert = True
                status_row.label(text="Objects Selected - Tools Active", icon='OBJECT_DATAMODE')
            else:
                status_row.label(text="No Objects Selected - Select Something First", icon='RESTRICT_SELECT_ON')
            
            # THE WHY - What is the 3D Cursor?
            if scene.show_help_cursor:
                col.label(text="3D Cursor = Universal Reference Point")
                col.label(text="Use it to: Position • Snap • Create • Measure")
                #col.separator()
            
                # Show the cursor visually
            col.prop(context.space_data.overlay, "show_cursor", text="Show 3D Cursor in Viewport")
            
            col.separator()
            col.label(text="KEY COMBINATION FOR ALL BELOW - (Shift + S)")
                # INVERSE PAIRS - clearly labeled
            if scene.show_help_cursor:
                col.label(text="Move TO 3D Cursor ↔ Move FROM 3D Cursor:")
           
            # Reset option
            row = col.row()
            row.scale_y = 1.5
            row.operator("view3d.snap_cursor_to_center", text="Reset Cursor to World Origin (0,0,0)")      
            
            col.separator()
            col.separator()
            col.label(text="INVERSE PAIRS:")
            col.separator()
            # Objects
            col.label(text="• 3D Cursor ↔ Object Origin:")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Object Origin")
            row.operator("object.origin_set", text="Object Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
            
            col.separator()
            col.separator()
            # Objects
            col.label(text="• 3D Cursor ↔ Object (Geometry):")
            row = col.row()
            #row.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Object")
            row.operator("shortcuts.cursor_to_geometry_center", text="3D Cursor to Object")
            #row.operator("view3d.snap_selected_to_cursor", text="Object to 3D Cursor")
            row.operator("shortcuts.object_geometry_to_cursor", text="Object to 3D Cursor")
            
            col.separator()
            col.separator()
            # Vertices (Edit Mode)
            col.label(text="• 3D Cursor ↔ Vertices (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Vertex")
            row.operator("view3d.snap_selected_to_cursor", text="Vertex to 3D Cursor")
            
            col.separator()
            col.separator()
            # Edges (Edit Mode)
            col.label(text="• 3D Cursor ↔ Edges (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Edge")
            row.operator("view3d.snap_selected_to_cursor", text="Edge to 3D Cursor")
            
            col.separator()
            col.separator()
            # Faces (Edit Mode)
            col.label(text="• 3D Cursor ↔ Faces (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Face")
            row.operator("view3d.snap_selected_to_cursor", text="Face to 3D Cursor")
            
            col.separator()
            col.separator()  


        # 🧩 World Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_world_origin", text="WORLD ORIGIN", emboss=False, icon='ORIENTATION_GLOBAL')
        
        row.prop(scene, "show_help_world_origin", text="", icon='HELP' if scene.show_help_world_origin else 'HIDE_ON', toggle=True)
        
        
        if scene.show_world_origin:
            col = box.column(align=True)
            
            # THE WHY - What is World Origin?
            if scene.show_help_world_origin:
                col.label(text="World Origin = The Center of Your 3D Space")
                col.label(text="Located at coordinates (0,0,0)")
                col.label(text="Reference point for everything in your scene")
                col.separator()
            
            
            # 3D CURSOR CONTROL
            if scene.show_help_world_origin:
                col.label(text="3D Cursor (The Red & White Target):")
            row = col.row()
            row.scale_y = 1.2
            row.operator("view3d.snap_cursor_to_center", text="Reset 3D Cursor to World Origin (Shift + S)")
            
            
            if scene.show_help_world_origin:
                col.label(text="• 3D Cursor marks where new objects appear")
                col.label(text="• Move cursor anywhere (Shift + RMB)")
            col.separator()
            
            # MOVING OBJECTS TO WORLD ORIGIN
            if scene.show_help_world_origin:
                col.label(text="Move Objects to World Origin:")
            
            row = col.row()
            row.scale_y = 1.2            
            row.operator("object.location_clear", text="Move Selected to World Origin (Alt + G)").clear_delta = False
            #col.operator("object.rotation_clear", text="Reset Selected Rotation").clear_delta = False
            #col.operator("object.scale_clear", text="Reset Selected Scale").clear_delta = False
            if scene.show_help_world_origin:
                col.label(text="• Location: Moves object to (0,0,0)")
                #col.label(text="• Rotation: Straightens object")
                #col.label(text="• Scale: Returns to original size")
            
            col.separator()
            col.separator()


        # 🧩 Object Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_origin", text="OBJECT ORIGIN", emboss=False, icon='OBJECT_ORIGIN')
        
        row.prop(scene, "show_help_object_origin", text="", icon='HELP' if scene.show_help_object_origin else 'HIDE_ON', toggle=True)
        
        
        if scene.show_object_origin:
            col = box.column(align=True)
            is_edit_mode = bpy.context.mode == 'EDIT_MESH'        
            
            # Selection status button
            status_row = col.row()
            if context.selected_objects:
                status_row.alert = True
                status_row.label(text="Objects Selected - Tools Active", icon='OBJECT_DATAMODE')
            else:
                status_row.label(text="No Objects Selected - Select Something First", icon='RESTRICT_SELECT_ON')
            
            col.separator()
            # Maybe add this at the start of Object Origin:
            if scene.show_help_object_origin:
                col.label(text="Object Origin = Pivot Point for:")
                col.label(text="Rotation • Scaling • Position for the selected object")
                col.separator()
            
            col.label(text="VIEWING CONTROLS:")
            # Add this at the top of Object Origin section:
            
            col.prop(context.space_data.overlay, "show_object_origins", text="Show All Object Origins")
            if scene.show_help_object_origin:   
                col.label(text="Show Origins in Viewport:")
            
            col.separator()
            col.separator()
            # Add these explanatory operations:
            col.label(text="Find & See Origins:")
            col.operator("view3d.view_selected", text="Focus View on Selected Object (Period .)")
            
            col.separator()
            col.separator()
            col.label(text="OBJECT ORIGIN TOOLS:")
            
            col.label(text="Object Origin Placement Options:")
            col.operator("object.origin_set", text="Origin to Center of Mass").type = 'ORIGIN_CENTER_OF_MASS'
            col.operator("object.origin_set", text="Origin to Bounding Box Center").type = 'ORIGIN_CENTER_OF_VOLUME'
            #col.operator("object.origin_set", text="Origin to Bottom of Object").type = 'ORIGIN_GEOMETRY'
            col.operator("mesh.origin_to_bottom", text="Origin to Bottom of Object")
            col.separator()
            
            col.label(text="ORIGIN POSITION:")
            if scene.show_help_object_origin:
                col.label(text="Select your object first")
                col.label(text="Shift + RMB to place your cursor")
                col.label(text="Click one of the buttons to reposition your object")
                col.separator()


            col.operator("mesh.top_origin_to_cursor", text="Top Origin to 3D Cursor")
            
            col.separator()
            col.operator("mesh.bottom_origin_to_cursor", text="Bottom Origin to 3D Cursor")
            
            col.separator()
            col.operator("mesh.front_origin_to_cursor", text="Front Origin to 3D Cursor")
            
            col.separator()
            col.operator("mesh.back_origin_to_cursor", text="Back Origin to 3D Cursor")
            
            col.separator()
            col.operator("mesh.left_origin_to_cursor", text="Left Origin to 3D Cursor")
            
            col.separator()
            col.operator("mesh.right_origin_to_cursor", text="Right Origin to 3D Cursor")
            
 
            col.separator()
            # Object Origin ↔ Global Zero
            col.label(text="Object Origin ↔ World Zero:")
            col.operator("mesh.origin_to_global_zero", text="Object Origin to World Zero")
            col.enabled = not is_edit_mode
            
            col.separator()
            col.separator()
            col.label(text="INVERSE PAIRS:")
            if scene.show_help_object_origin:   
                col.label(text="These commands below are grouped by two way relationship")
  

            col.separator()   
            # Object Origin ↔ 3D Cursor
            col.label(text="Object Origin ↔ 3D Cursor:")
            col.operator("object.origin_set", text="Object Origin to 3D Cursor").type = 'ORIGIN_CURSOR'
            col.operator("view3d.snap_cursor_to_selected", text="3D Cursor to Object Origin")
        
            col.separator()
            col.separator() 
            # Object Origin ↔ Object Geometry
            col.label(text="Object Origin ↔ Object Geometry:")
            col.operator("object.origin_set", text="Object Origin to Object Geometry").type = 'ORIGIN_GEOMETRY'
            #col.enabled = not is_edit_mode
            col.operator("object.origin_set", text="Object Geometry to Object Origin").type = 'GEOMETRY_ORIGIN'
      
            col.separator()
            col.separator()
        
        
        # 🧩 Primitives
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_primitives", text="PRIMITIVES", emboss=False, icon='MESH_CUBE')

        row.prop(scene, "show_help_primitives", text="", icon='HELP' if scene.show_help_primitives else 'HIDE_ON', toggle=True)

        if scene.show_primitives:
            col = box.column(align=True)
            
            if scene.show_help_primitives:
                col.label(text="Basic shapes to start modeling with:")
                col.separator()
            
            # Basic primitives
            col.operator("mesh.primitive_plane_add", text="Plane", icon='MESH_PLANE')
            if scene.show_help_primitives:
                col.label(text="• Flat surface (good for floors, walls)")
            
            col.operator("mesh.primitive_cube_add", text="Cube", icon='MESH_CUBE')
            if scene.show_help_primitives:
                col.label(text="• Basic box shape")
            
            col.operator("mesh.primitive_circle_add", text="Circle", icon='MESH_CIRCLE')
            if scene.show_help_primitives:
                col.label(text="• Flat circle (good for starting complex shapes)")
            
            col.operator("mesh.primitive_uv_sphere_add", text="Sphere", icon='MESH_UVSPHERE')
            if scene.show_help_primitives:
                col.label(text="• Perfect ball shape")
            
            col.operator("mesh.primitive_cylinder_add", text="Cylinder", icon='MESH_CYLINDER')
            if scene.show_help_primitives:
                col.label(text="• Tube shape (good for pillars, cans)")
            
            col.operator("mesh.primitive_cone_add", text="Cone", icon='MESH_CONE')
            if scene.show_help_primitives:
                col.label(text="• Pointed cone shape")
            
            col.operator("mesh.primitive_torus_add", text="Torus", icon='MESH_TORUS')
            if scene.show_help_primitives:
                col.label(text="• Donut shape")
            
            if scene.show_help_primitives:
                col.separator()
                col.label(text="💡 Tip: All primitives appear at 3D cursor location")

        # Don't forget to add these properties to your PropertyGroup:
        # show_primitives: BoolProperty(name="Show Primitives", default=True)
        # show_help_primitives: BoolProperty(name="Show Primitives Help", default=False)
        
        
        # 🧩 Object Mode
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_mode", text="OBJECT MODE", emboss=False, icon='OBJECT_DATAMODE')
        
        row.prop(scene, "show_help_object_mode", text="", icon='HELP' if scene.show_help_object_mode else 'HIDE_ON', toggle=True)
        
        
        if scene.show_object_mode:
            col = box.column(align=True)
            
            # Selection status button
            status_row = col.row()
            if context.selected_objects:
                status_row.alert = True
                status_row.label(text="Objects Selected - Tools Active", icon='OBJECT_DATAMODE')
            else:
                status_row.label(text="No Objects Selected - Select Something First", icon='RESTRICT_SELECT_ON')
            
            # THE WHY - What is Object Mode?
            if scene.show_help_object_mode:
                col.label(text="Object Mode = Work with Whole Objects")
                col.label(text="Move, copy, delete, join, boolean entire objects")
                col.separator()            
                
            col.separator()
            col.separator()
            col.label(text="Apply Selected Transforms:")  
            
            row = col.row()
            row.scale_y = 1.35
            row.operator("object.transform_apply", text="Apply Rotation and Scale (Ctrl + A)")
            if scene.show_help_general:
                col.label(text="• Apply Transforms: Makes current rotation/scale permanent")
                col.label(text="• Used after Rotation and Scaling")
            
            col.separator()            
            # New section: Apply Scale & Apply Rotation
            row = col.row()  # Create a new row for the apply buttons

            # Apply Rotation only  
            sub_row = row.row()
            op = sub_row.operator("object.transform_apply", text="Apply Rotation")
            op.location = False
            op.rotation = True
            op.scale = False

            # Apply Scale only
            sub_row = row.row()
            op = sub_row.operator("object.transform_apply", text="Apply Scale")
            op.location = False
            op.rotation = False
            op.scale = True

                        
            
            col.separator()
            col.label(text="Reset Selected Transforms:")    
            
            
            # Combined Reset Button
            row = col.row()
            row.scale_y = 1.35
            row.operator("object.reset_transforms", text="Reset Rotation & Scale")
            
            col.separator()
            # New section: Reset Rotation & Reset Scale
            row = col.row()  # Create a new row for the reset buttons

            # Reset Rotation
            sub_row = row.row()
            sub_row.operator("object.rotation_clear", text="Reset Rotation (Alt + R)").clear_delta = False
            
            # Reset Scale
            sub_row = row.row()
            sub_row.operator("object.scale_clear", text="Reset Scale (Alt + S)").clear_delta = False           
            
            
            
            if scene.show_help_general:
                col.label(text="• Reset Rotation: Straightens object")
                col.label(text="• Reset Scale: Returns to original size")
                col.label(text="• Undo Transforms: Removes current rotation/scale")
            
       
            col.separator()
            col.separator()
            col.label(text="VIEWING CONTROLS:")
            col.label(text="Object Visibility:")              
            col.operator("object.hide_view_set", text="Hide Selected (H)")
            col.operator("object.hide_view_clear", text="Reveal Hidden (Alt + H)")
            
            col.separator()
            col.separator()
            # APPEARANCE
            col.label(text="Object Preview:")
            col.operator("object.shade_smooth", text="Object Shade Smooth")
            if scene.show_help_object_mode:
                col.label(text="• Smooth = Curved surfaces")
            col.operator("object.shade_flat", text="Object Shade Flat")
            if scene.show_help_object_mode:
                col.label(text="• Flat = Angular surfaces")
                
            col.separator()
            col.separator()
            # SELECTION (Most Basic)
            col.label(text="Object Selection:")
            col.operator("object.select_all", text="Select All/Deselect All (A)")
            if scene.show_help_object_mode:
                col.label(text="• Click object to select")
                col.label(text="• Shift+Click to select multiple")
                col.separator()
                
                
            col.operator("object.select_all", text="Select All/None (A)")
            if scene.show_help_edit_mode:    
                col.label(text="• Select All/None = Toggle all selection")
                
            if hasattr(bpy.ops.object, 'select_all'):
                col.operator("object.select_all", text="Select Opposite (Ctrl + I)").action = 'INVERT'  
            if scene.show_help_edit_mode:    
                col.label(text="• Select Opposite = Invert current selection")
            
            col.separator()
            col.separator()
            col.label(text="OBJECT TOOLS:")             
        
            col.separator()
            # BASIC OBJECT OPERATIONS
            col.label(text="Basic Operations:")
            col.operator("object.duplicate_move", text="Duplicate (Shift + D)")
            if scene.show_help_object_mode:
                col.label(text="• Duplicate: Creates copy you can move")
            col.operator("object.make_single_user", text="Make Unique [single user] (U)")
            if scene.show_help_object_mode:
                col.label(text="• Make unique as its own object")
                col.label(text="• Keep seperate mesh and textures")
            col.operator("object.delete", text="Delete (X or Delete)")
            if scene.show_help_object_mode:
                col.label(text="• Delete: Removes object completely")
                col.separator()
            
            col.separator()
            col.separator()
            # COMBINING OBJECTS
            col.label(text="Combine Objects:")
            col.operator("object.join", text="Join into One Object (Ctrl + J)")
            if scene.show_help_object_mode:
                col.label(text="• Select multiple objects first")
                col.label(text="• Last selected becomes the result")
                col.separator()
          
                
            col.separator()
            col.separator()
            # MODIFIERS
            col.label(text="Modifier: Stack (Properties > Green spanner)")

            # Bevel Modifier
            op = col.operator("object.modifier_add", text="Bevel Modifier")
            op.type = 'BEVEL'
            if scene.show_help_edit_mode:    
                col.label(text="• Add Bevel Modifier")

            # Boolean Modifier    
            op = col.operator("object.modifier_add", text="Boolean Modifier")
            op.type = 'BOOLEAN'
            if scene.show_help_edit_mode:    
                col.label(text="• Add Boolean Modifier")

            # Decimate Modifier
            op = col.operator("object.modifier_add", text="Decimate Modifier")
            op.type = 'DECIMATE'
            if scene.show_help_edit_mode:    
                col.label(text="• Add Decimate Modifier")

            # Mirror Modifier
            op = col.operator("object.modifier_add", text="Mirror Modifier")
            op.type = 'MIRROR'
            if scene.show_help_edit_mode:    
                col.label(text="• Add Mirror Modifier")

            # Solidify Modifier
            op = col.operator("object.modifier_add", text="Solidify Modifier")
            op.type = 'SOLIDIFY'
            if scene.show_help_edit_mode:    
                col.label(text="• Add Solidify Modifier")
            
            col.separator()
            col.separator()
            col.label(text="Sub-Division Modifier: Level 1, 2, 3 ")
            
            op = col.operator("object.subdivision_set", text="Sub Divide Mesh Level 1 (Ctrl + 1)")
            op.level = 1
            op.relative = False
            if scene.show_help_edit_mode:    
                col.label(text="• Create Modifier = Level 1")

            col.operator("object.subdivision_set", text="Sub Divide Mesh Level 2 (Ctrl + 2)")
            op.level = 2
            op.relative = False
            if scene.show_help_edit_mode:    
                col.label(text="• Create Modifier = Level 2")
            
            col.operator("object.subdivision_set", text="Sub Divide Mesh Level 3 (Ctrl + 3)")
            op.level = 3
            op.relative = False
            if scene.show_help_edit_mode:    
                col.label(text="• Create Modifier = Level 3")
            
            col.operator("object.make_links_data", text="Copy Modifiers - from > to (Ctrl + L)").type='MODIFIERS'
            if scene.show_help_edit_mode:    
                col.label(text="• Copy Modifiers = from (1st selection) to (shift click 2nd selection")
            
            #col.label(text="Separate:")
            #col.operator("mesh.separate", text="Separate Parts (P)")
            #if scene.show_help_edit_mode:    
                #col.label(text="• Separate = Break into separate objects")
            
            
            col.separator()
            col.separator()
            # ORGANIZATION
            col.label(text="Organization:")
            col.operator("object.move_to_collection", text="Move to Collection (M)")
            col.operator("object.hide_viewport", text="Hide Selected (H)")
            col.operator("object.hide_viewport_unselected", text="Unhide All (Alt + H)")
            if scene.show_help_object_mode:
                col.label(text="• Collections = Folders for objects")
            
            col.separator()
            col.separator()

            


        # 🧩 Edit Mode  
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_edit_mode", text="EDIT MODE", emboss=False, icon='EDITMODE_HLT')
        
        row.prop(scene, "show_help_edit_mode", text="", icon='HELP' if scene.show_help_edit_mode else 'HIDE_ON', toggle=True)
        
        
        if scene.show_edit_mode:
            col = box.column(align=True)
            
            # Selection status for Edit Mode
            # Selection status for Edit Mode
            # Selection status for Edit Mode
            status_row = col.row()
            obj = context.active_object
            if obj and obj.mode == 'EDIT' and obj.type == 'MESH':
                import bmesh
                bm = bmesh.from_edit_mesh(obj.data)
                
                # Check what type of elements are selected
                selected_verts = [v for v in bm.verts if v.select]
                selected_edges = [e for e in bm.edges if e.select]  
                selected_faces = [f for f in bm.faces if f.select]
                
                if selected_faces:
                    status_row.alert = True
                    status_row.label(text="Faces Selected - Tools Active", icon='FACESEL')
                elif selected_edges:
                    status_row.alert = True
                    status_row.label(text="Edges Selected - Tools Active", icon='EDGESEL')
                elif selected_verts:
                    status_row.alert = True
                    status_row.label(text="Vertices Selected - Tools Active", icon='VERTEXSEL')
                else:
                    status_row.label(text="No Elements Selected - Verts/Edges/Faces", icon='RESTRICT_SELECT_ON')
            else:
                status_row.label(text="Enter Edit Mode to Select Elements", icon='EDITMODE_HLT')
    
            
            # THE WHY - What is Edit Mode?
            if scene.show_help_edit_mode:
                col.label(text="Edit Mode = Modify Object Mesh")
                col.label(text="Work with VERTICES, EDGES, FACES")
                
                col.separator()
            
                # SELECTION MODES
                col.label(text="Selection Modes:")
                col.label(text="KEY 1 = Vertex mode (points)")
                col.label(text="KEY 2 = Edge mode (lines)")  
                col.label(text="KEY 3 = Face mode (surfaces)")
                col.separator()
            
            # Keep visibility controls at top
            col.label(text="VIEWING CONTROLS:")
            col.label(text="Mesh Visibility:")
            col.operator("mesh.hide", text="Hide Selected (H)")
            col.operator("mesh.reveal", text="Reveal Hidden (Alt + H)")
            
            col.separator()
            col.separator()
            col.label(text="Mesh Preview:")
            col.operator("mesh.faces_shade_smooth", text="Mesh Shade Smooth (Ctrl + F)")
            if scene.show_help_edit_mode:    
                col.label(text="• Shade Smooth = Soft rounded shading")
            col.operator("mesh.faces_shade_flat", text="Mesh Shade Flat (Ctrl + F)")
            if scene.show_help_edit_mode:    
                col.label(text="• Shade Flat = Hard angular shading")
            
            
            col.separator()
            col.separator()
            # SELECTION
            col.label(text="Mesh Selection:")
            col.operator("mesh.select_all", text="Select All/None (A)")
            if scene.show_help_edit_mode:    
                col.label(text="• Select All/None = Toggle all selection")
                
            if hasattr(bpy.ops.mesh, 'select_all'):
                col.operator("mesh.select_all", text="Select Opposite (Ctrl + I)").action = 'INVERT'  
            if scene.show_help_edit_mode:    
                col.label(text="• Select Opposite = Invert current selection")
            
            col.operator("mesh.select_more", text="Grow Selection (Ctrl + +)")
            if scene.show_help_edit_mode:    
                col.label(text="• Grow Selection = Expand selection area")
            col.operator("mesh.select_less", text="Shrink Selection (Ctrl + -)")
            if scene.show_help_edit_mode:    
                col.label(text="• Shrink Selection = Reduce selection area")
            
            col.operator("mesh.select_linked", text="Select Linked (L)")
            if scene.show_help_edit_mode:    
                col.label(text="• Select Connected = Select all connected geometry")
            
            col.separator()
            col.separator()
            # Correct coplanar selection
            col.label(text="Select Similar - Shift + G")
            #op = col.operator("mesh.select_similar", text="Select Similar - Coplanar (Shift + G)")
            #op.type = 'COPLANAR'
            #if scene.show_help_edit_mode:    
            col.label(text="• Sub menu changes depending on vertice, edge or face selected")
            
            
            
            
            
            col.separator()
            col.separator()
            col.label(text="EDITING TOOLS:")
            if scene.show_help_edit_mode: 
                col.label(text="Right click on the object to see the tool menu")
                col.separator()
            # CLEANUP
            col.label(text="Cleanup:")
            col.operator("mesh.beautify_fill", text="Beautify Faces (Ctrl + F)")
            if scene.show_help_edit_mode:    
                col.label(text="• Beautify = Improve face topology")
            col.operator("mesh.delete_loose", text="Delete Loose Geometry")
            if scene.show_help_edit_mode:    
                col.label(text="• Delete Loose = Remove unconnected vertices/edges")
            col.operator("mesh.merge", text="Merge Vertices (M)")
            if scene.show_help_edit_mode:    
                col.label(text="• Merge = Merge vertices into one")
            col.operator("mesh.tris_convert_to_quads", text="Tris to Quads (Alt + J)")
            if scene.show_help_edit_mode:    
                col.label(text="• Tris to Quads = Convert triangles to quads")
            col.operator("mesh.remove_doubles", text="Remove Duplicates (M)")
            if scene.show_help_edit_mode:    
                col.label(text="• Merge: By Distance = Remove duplicate vertices")
            
            col.separator()
            col.separator()
            # DISSOLVE
            col.label(text="Dissolve:")
            col.operator("mesh.dissolve_verts", text="Dissolve Vertices (X)")
            if scene.show_help_edit_mode:    
                col.label(text="• Dissolve Vertices = Remove vertices, keep connections")
            
            col.operator("mesh.dissolve_edges", text="Dissolve Edges (X)")
            if scene.show_help_edit_mode:    
                col.label(text="• Dissolve Edges = Remove edges, keep faces")
            col.operator("mesh.dissolve_faces", text="Dissolve Faces (X)")
            if scene.show_help_edit_mode:    
                col.label(text="• Dissolve Faces = Remove faces, keep edges")
            col.operator("mesh.dissolve_limited", text="Limited Dissolve (X)")
            if scene.show_help_edit_mode:    
                col.label(text="• Limited Dissolve = Remove unnecessary edges/faces")
            
            col.separator()
            col.separator()
            # DUPLICATION
            col.label(text="Duplication:")
            col.operator("mesh.duplicate_move", text="Duplicate (Shift+D)")
            if scene.show_help_edit_mode:    
                col.label(text="• Duplicate = Copy selected geometry")
            
            col.separator()
            col.separator()
            # EDGE TOOLS
            col.label(text="Edge Tools:")
            col.operator("mesh.bevel", text="Bevel Edges/Vertices (Ctrl+B)")
            if scene.show_help_edit_mode:
                col.label(text="• Bevel = Add bevel or chamfer (Mouse drag and wheel)")
            col.operator("mesh.bridge_edge_loops", text="Bridge Edge Loops (Ctrl + E)")
            if scene.show_help_edit_mode:
                col.label(text="• Bridge = Connect two edge loops with faces")
            if hasattr(bpy.ops.mesh, 'loopcut_slide'):
                col.operator("mesh.loopcut_slide", text="Loop Cut (Ctrl + R)")
                if scene.show_help_edit_mode:    
                    col.label(text="• Loop Cut = Add edge ring around object")
            col.operator("mesh.mark_seam", text="Mark Seam (Ctrl + E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Mark Seam = Mark edges for UV unwrapping")
            col.operator("mesh.mark_sharp", text="Mark Sharp (Ctrl + E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Mark Sharp = Mark edges for hard shading")
            col.operator("mesh.rip_edge", text="Rip Edge (Alt + V)")
            if scene.show_help_edit_mode:    
                col.label(text="• Rip Edge = Split edge into two")
            col.operator("mesh.subdivide", text="Subdivide Edges (Ctrl + E)(RMB > S)")
            if scene.show_help_edit_mode:    
                col.label(text="• Subdivide = Add cuts to increase edge density")
            col.operator("mesh.unsubdivide", text="Unsubdivide (Ctrl + E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Quick Unsubdivide")
            col.separator()
            col.label(text="• Edge Slide along face (gg)")
            
            col.separator()
            col.separator()
            # EXTRUDE
            col.label(text="Extrude:")
            col.operator("mesh.extrude_region_move", text="Extrude (E)")
            if scene.show_help_edit_mode:
                col.label(text="• Extrude = Pull out new geometry")
            col.operator("mesh.extrude_vertices_move", text="Extrude Vertices (E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Extrude Vertices = Pull out new vertices")
            col.operator("mesh.extrude_edges_move", text="Extrude Edges (E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Extrude Edges = Pull out new edges")
            col.operator("mesh.extrude_faces_move", text="Extrude Faces (E)")
            if scene.show_help_edit_mode:    
                col.label(text="• Extrude Faces = Pull out new faces")
            
            col.operator("mesh.inset", text="Inset Faces (I)")
            if scene.show_help_edit_mode:    
                col.label(text="• Inset = Push in new geometry")
            col.separator()
            col.label(text="• Extrude Advanced (Alt + E):")
            if scene.show_help_edit_mode:
                col.label(text="Example:")
                col.label(text="Extrude Normal (Alt + E) > Extrude faces along Normals:")
            
            col.separator()
            col.separator()
            # FACE TOOLS
            col.label(text="Face Tools:")
            col.operator("mesh.fill", text="Fill Faces/Holes (F)")
            if scene.show_help_edit_mode:    
                col.label(text="• Fill = Fill holes with new faces")
            col.operator("mesh.fill_grid", text="Fill with Grid (Ctrl + F)")
            if scene.show_help_edit_mode:    
                col.label(text="• Fill Grid = Fill empty area with quad grid")
            
            col.separator()
            col.separator()
            
            
            # KNIFE
            col.label(text="Knife:")
            col.operator("mesh.knife_tool", text="Knife Tool (K)")
            if scene.show_help_edit_mode:    
                col.label(text="• Knife = Cut custom lines through mesh")
            
          
                        
            col.separator()
            col.separator()
            # SPLIT & SEPARATE
            col.label(text="Split & Separate:")
            col.operator("mesh.rip", text="Rip Vertices (V)")
            if scene.show_help_edit_mode:    
                col.label(text="• Rip = Split vertex into two")
            col.operator("mesh.separate", text="Separate Parts (P)")
            if scene.show_help_edit_mode:    
                col.label(text="• Separate = Break into separate objects")
            col.operator("mesh.split", text="Split Geometry (Y)")
            if scene.show_help_edit_mode:    
                col.label(text="• Split = Separate vertices while keeping position")
            
            col.separator()
            col.separator()
            # TRANSFORM
            col.label(text="Transform:")
            if hasattr(bpy.ops.transform, 'shrink_fatten'):
                col.operator("transform.shrink_fatten", text="Shrink/Fatten (Alt + S)")
                if scene.show_help_edit_mode:    
                    col.label(text="• Shrink/Fatten = Move along surface normals")
            
            col.separator()
            col.separator()



            
        # 🧩 Camera
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_camera", text="CAMERA", emboss=False, icon='CAMERA_DATA')
        
        row.prop(scene, "show_help_camera", text="", icon='HELP' if scene.show_help_camera else 'HIDE_ON', toggle=True)
        
        
        if scene.show_camera:
            col = box.column(align=True)
            
            col.separator()
            # ADVANCED NAVIGATION
            col.label(text="Advanced Navigation:")
            col.operator("view3d.walk", text="Walk Mode (Shift + `)")
            
            
            
            # CAMERA LOCK (Advanced but Important)
            col.label(text="Camera Lock:")
            if hasattr(context.space_data, 'lock_camera'):
                col.prop(context.space_data, "lock_camera", text="Lock Camera to View")
                if scene.show_help_camera:
                    col.label(text="• When locked: Moving view = moving camera")
                    col.label(text="• When unlocked: Camera stays put")
            
            col.separator()
            col.separator()
            # THE WHY - What is a Camera?
            if scene.show_help_camera:
                col.label(text="Camera = What Will Be Rendered")
                col.label(text="Every scene needs a camera to create final images")
                col.separator()
            
            # CAMERA STATUS CHECK
            if context.scene.camera:
                col.label(text=f"Active Camera: {context.scene.camera.name}")
            else:
                col.label(text="⚠ No Active Camera in Scene")
                col.operator("object.camera_add", text="Add Camera to Scene")
                col.separator()
                pass  # Don't show other options if no camera
            
            col.separator()
            col.separator()
            # CAMERA VIEWING
            col.label(text="Camera View:")
            col.operator("view3d.view_camera", text="Look Through Camera (Numpad 0)")
            if scene.show_help_camera:
                col.label(text="• See exactly what will be rendered")
                col.separator()
            
            col.separator()
            col.separator()
            # CAMERA POSITIONING
            col.label(text="Position Camera:")
            col.operator("view3d.camera_to_view", text="Move Camera to Current View (Ctrl + Alt + Numpad 0)")
            if scene.show_help_camera:
                col.label(text="• First: Navigate to desired view")
                col.label(text="• Then: Use this to position camera there")
                col.separator()
            
            col.separator()
            col.separator()
            # CAMERA PROPERTIES
            col.label(text="Camera Settings:")
            if context.scene.camera and context.scene.camera.data:
                camera_data = context.scene.camera.data
                col.prop(camera_data, "lens", text="Focal Length (mm)")
                if scene.show_help_camera:
                    col.label(text="• Lower = Wider view (18mm = very wide)")
                    col.label(text="• Higher = Narrower view (85mm = portrait)")
                    col.separator()
                
                col.separator()
                col.separator()
                # Depth of Field toggle
                col.prop(camera_data.dof, "use_dof", text="Depth of Field (Blur)")
                if camera_data.dof.use_dof:
                    col.prop(camera_data.dof, "aperture_fstop", text="F-Stop (Blur Amount)")
                    col.prop(camera_data.dof, "focus_distance", text="Focus Distance")
            
            col.separator()
            col.separator()
            # CAMERA SELECTION
            col.label(text="Camera Object:")
            col.operator("object.select_camera", text="Select Camera Object")
            if scene.show_help_camera:
                col.label(text="• Select to move/rotate like any object")
            
            col.separator()
            col.separator()
            # MULTIPLE CAMERAS
            cameras_in_scene = [obj for obj in context.scene.objects if obj.type == 'CAMERA']
            if len(cameras_in_scene) > 1:
                col.separator()
                col.label(text="Multiple Cameras:")
                for cam in cameras_in_scene:
                    row = col.row()
                    op = row.operator("scene.camera_set", text=f"Set {cam.name} as Active")
                    op.camera = cam.name
            else:
                col.separator()
                col.operator("object.camera_add", text="Add Another Camera")
                if scene.show_help_camera:
                    col.label(text="• Use multiple cameras for different shots")            

            col.separator()
            col.separator()

        # 🧩 Render
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_render", text="RENDER", emboss=False, icon='RENDER_STILL')
        
        row.prop(scene, "show_help_render", text="", icon='HELP' if scene.show_help_render else 'HIDE_ON', toggle=True)
        
        if scene.show_render:
            col = box.column(align=True)
            
            # THE WHY - What is Rendering?
            if scene.show_help_render:
                col.label(text="Render = Create Final Image/Video")
                col.label(text="Converts 3D scene into 2D picture")
                col.separator()
            
            # RENDER ENGINE
            col.label(text="Render Engine:")
            col.prop(context.scene.render, "engine", text="")
            if context.scene.render.engine == 'BLENDER_EEVEE':
                if scene.show_help_render:
                    col.label(text="• Eevee = Fast, good for previews")
            elif context.scene.render.engine == 'CYCLES':
                if scene.show_help_render:
                    col.label(text="• Cycles = Slow, photorealistic")
            elif context.scene.render.engine == 'BLENDER_WORKBENCH':
                if scene.show_help_render:
                    col.label(text="• Workbench = Very fast, simple")
            
            col.separator()
            col.separator()
            # RENDER ACTIONS
            col.label(text="Render Actions:")
            col.operator("render.render", text="Render Image (F12)")
            col.operator("render.view_show", text="View Last Render (F11)")
            
            col.separator()
            col.separator()
            # ANIMATION
            col.label(text="Animation:")
            col.operator("render.render", text="Render Animation (Ctrl + F12)").animation = True
            col.operator("render.play_rendered_anim", text="Play Rendered Animation")
            
            col.separator()
            col.separator()
            # OUTPUT SETTINGS
            col.label(text="Output Settings:")
            col.prop(context.scene.render, "resolution_x", text="Width")
            col.prop(context.scene.render, "resolution_y", text="Height")
            col.prop(context.scene.render, "resolution_percentage", text="Quality %")
            if scene.shortcuts_show_help:
                col.label(text="• 100% = Full quality, 50% = Half size")
            
            col.separator()
            col.separator()
            # FILE FORMAT
            col.label(text="File Format:")
            col.prop(context.scene.render.image_settings, "file_format", text="")
            col.prop(context.scene.render, "filepath", text="Save Location")
            
            col.separator()
            col.separator()
            # SAMPLING (For Cycles/Eevee)
            if context.scene.render.engine in ['CYCLES', 'BLENDER_EEVEE']:
                col.label(text="Quality Settings:")
                if context.scene.render.engine == 'CYCLES':
                    col.prop(context.scene.cycles, "samples", text="Samples")
                    col.label(text="• More samples = Better quality + Slower")
                elif context.scene.render.engine == 'BLENDER_EEVEE':
                    col.prop(context.scene.eevee, "taa_render_samples", text="Samples")
            
            col.separator()
            col.separator()
            # VIEWPORT RENDER
            col.label(text="Quick Preview:")
            col.operator("render.opengl", text="Viewport Render (Current View)")
            if scene.shortcuts_show_help:
                col.label(text="• Fast render of current viewport")
            
            col.separator()
            col.separator()
            # RENDER REGION
            col.label(text="Partial Render:")
            col.operator("view3d.render_border", text="Set Render Border (Ctrl + B)")
            col.prop(context.scene.render, "use_border", text="Use Border")
            if scene.show_help_render:
                col.label(text="• Render only part of image (faster testing)")
            
            col.separator()
            col.separator()
            # COMMON ISSUES
            col.label(text="Common Issues:")
            col.label(text="• Black render = No lights in scene")
            col.label(text="• Noisy render = Increase samples")
            col.label(text="• Slow render = Lower samples/resolution")
            
            col.separator()
            col.separator()
            # LIGHTING CHECK
            lights_in_scene = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
            if not lights_in_scene and context.scene.render.engine != 'BLENDER_WORKBENCH':
                col.label(text="⚠ No Lights in Scene")
                col.operator("object.light_add", text="Add Light").type = 'SUN'
            else:
                col.label(text=f"✓ {len(lights_in_scene)} Light(s) in Scene")
            
            col.separator()
            col.separator()
            # MATERIAL CHECK
            if context.active_object and context.active_object.type == 'MESH':
                if not context.active_object.material_slots:
                    col.label(text="⚠ No Materials on Active Object")
                    col.operator("object.material_slot_add", text="Add Material Slot")
                else:
                    col.label(text="✓ Materials Present")
            
            col.separator()
            col.separator()
            
            
        # 🧩 About
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_about", text="ABOUT", emboss=False, icon='INFO')
        
        row.prop(scene, "show_help_about", text="", icon='HELP' if scene.show_help_about else 'HIDE_ON', toggle=True)
        
        if scene.show_about:
            col = box.column(align=True)
            
            # HEADER WITH LOGO SPACE
            header_box = col.box()
            header_col = header_box.column(align=True)
            header_col.scale_y = 1.2
            header_col.label(text="🎯 BLENDER CHEATSHEETS", icon='COMMUNITY')
            header_col.label(text="Making Blender Accessible for Everyone")
            
            col.separator()
            col.separator()
            # MISSION STATEMENT
            mission_box = col.box()
            mission_col = mission_box.column(align=True)
            mission_col.label(text="📋 Our Mission:")
            mission_col.label(text="• Remove the learning curve barriers")
            mission_col.label(text="• Make Blender accessible to all ages")
            mission_col.label(text="• Provide transparent, easy-to-use tools")
            mission_col.label(text="• Use standard terminology")
            mission_col.label(text="• Expose hidden keyboard shortcuts")
            
            col.separator()
            col.separator()
            # VERSION INFO
            version_box = col.box()
            version_col = version_box.column(align=True)
            version_col.label(text="🔧 Version Info:")
            version_col.label(text="• Designed for Blender 3.6+ LTS")
            version_col.label(text="• Focus on core modeling essentials")
            version_col.label(text="• Free for life under GPLv2")
            version_col.label(text="• Regular updates for LTS versions")
            
            col.separator()
            col.separator()
            # DEVELOPER INFO
            dev_box = col.box()
            dev_col = dev_box.column(align=True)
            dev_col.label(text="🎮 DEAD DOG DOWN GAME STUDIO")
            dev_col.separator()
            
            # CLICKABLE WEBSITE
            website_row = dev_col.row()
            website_row.operator("wm.url_open", text="🌐 Visit Our Website", 
                                icon='URL').url = "https://deaddogdown.github.io/"
            
            # CLICKABLE EMAIL
            email_row = dev_col.row()
            email_row.operator("wm.url_open", text="✉️ Contact Us", 
                              icon='FILE_TEXT').url = "mailto:deaddogdown.gamestudio@gmail.com"
            
            col.separator()
            col.separator()
            # SUPPORT SECTION
            support_box = col.box()
            support_col = support_box.column(align=True)
            support_col.label(text="💝 Support This Project:")
            support_col.label(text="This addon is completely free, but")
            support_col.label(text="your support helps us maintain and")
            support_col.label(text="improve it for the community.")
            support_col.separator()
            
            # SUPPORT ACTIONS
            support_row = support_col.row(align=True)
            support_row.operator("wm.url_open", text="⭐ GitHub", 
                                icon='FILE_FOLDER').url = "https://github.com/deaddogdown"
            support_row.operator("wm.url_open", text="💰 Sponsor", 
                                icon='HEART').url = "mailto:deaddogdown.gamestudio@gmail.com?subject=Sponsorship"
            
            col.separator()
            col.separator()
            # INSPIRATIONAL FOOTER
            footer_box = col.box()
            footer_col = footer_box.column(align=True)
            footer_col.scale_y = 0.8
            footer_col.label(text="🚀 'Enjoy using Blender with new eyes'")
            footer_col.label(text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            footer_col.label(text="Making complex software simple, one tool at a time.")
            
            col.separator()
            col.separator()
            # VERSION/BUILD INFO (Optional)
            info_col = col.column(align=True)
            info_col.scale_y = 0.7
            info_col.label(text="Build: v1.0 | License: GPLv2 | Community Driven")
            
            col.separator()
            col.separator()

class SHORTCUTS_OT_ObjectMode(bpy.types.Operator):
    bl_idname = "object.switch_to_object_mode"
    bl_label = "Object Mode"
    bl_description = "Switch to Object Mode"
    
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class SHORTCUTS_OT_EditMode(bpy.types.Operator):
    bl_idname = "object.switch_to_edit_mode"
    bl_label = "Edit Mode"
    bl_description = "Switch to Edit Mode"
    
    def execute(self, context):
        if context.object and context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


classes = (
    SHORTCUTS_PT_Panel,
    SHORTCUTS_OT_SetUnits,
    SHORTCUTS_OT_ObjectMode,
    SHORTCUTS_OT_EditMode,
    SHORTCUTS_OT_CursorToGeometryCenter,
    SHORTCUTS_OT_ObjectGeometryToCursor,
    MESH_OT_front_origin_to_cursor,
    MESH_OT_back_origin_to_cursor,
    MESH_OT_top_origin_to_cursor,
    MESH_OT_bottom_origin_to_cursor, 
    MESH_OT_left_origin_to_cursor,
    MESH_OT_right_origin_to_cursor,
    OBJECT_OT_reset_transforms,
    MESH_OT_smart_snap_vertex,
    MESH_OT_smart_snap_edge,
    MESH_OT_smart_snap_face,
    MESH_OT_smart_snap,
)

def register():
    # Add the help toggle property to the scene FIRST
    bpy.types.Scene.shortcuts_show_help = BoolProperty(
        name="Show Help Text",
        description="Show or hide helpful descriptions for beginners",
        default=True  # Default to showing help for new users
    )
    
    register_properties()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    # Remove the property when unregistering
    if hasattr(bpy.types.Scene, 'shortcuts_show_help'):
        del bpy.types.Scene.shortcuts_show_help    
    unregister_properties()

if __name__ == "__main__":
    register()