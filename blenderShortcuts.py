import bpy

# Register collapsible section properties
def register_properties():
    props = [
        ('show_general', False),
        ('show_viewport', False),
        ('show_transform', False),
        ('show_world_origin', False),
        ('show_object_origin', False),
        ('show_cursor', False),
        ('show_object_mode', False),
        ('show_edit_mode', False),
        ('show_camera', False),        
        ('show_render', False),
        ('show_about', False)
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
        'show_world_origin',
        'show_object_origin',
        'show_cursor',
        'show_object_mode',
        'show_edit_mode',
        'show_camera',        
        'show_render',
        'show_about'
    ]
    for prop in props:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)

class SHORTCUTS_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "CheatSheets"
    bl_label = "CheatSheets"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
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

        layout.separator()
        
        

        # 🧩 General
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_general", text="General", emboss=False, icon='INFO')
        if scene.show_general:
            col = box.column(align=True)
            col.operator("wm.search_menu", text="Search Operators: F3 or Spacebar")
            col.operator("object.duplicate_move", text="Duplicate: Shift + D")
            col.operator("object.make_single_user", text="Make Unique: U")
            
            # Info labels for shortcuts that don't need operators:
            col.separator()
            col.label(text="Keyboard Shortcuts:")
            col.label(text="• Undo: Ctrl + Z")
            col.label(text="• Redo: Ctrl + Shift + Z")
            col.label(text="• Copy: Ctrl + C")
            col.label(text="• Paste: Ctrl + V")
            
        
        # 🧩 Viewport
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_viewport", text="Viewport", emboss=False, icon='VIEW_CAMERA')
        if scene.show_viewport:
            col = box.column(align=True)
            
            # THE WHY - What is the Viewport?
            col.label(text="Viewport = Your 3D Window")
            col.label(text="Navigate (move yourself) vs Transform (move objects)")
            col.separator()
            
            # MOUSE NAVIGATION (Most Important - Put First)
            col.label(text="Mouse Navigation:")
            col.label(text="• Orbit: Middle Mouse Button (MMB) Drag")
            col.label(text="• Pan: Shift + MMB Drag") 
            col.label(text="• Zoom: Scroll Wheel or Ctrl + MMB Drag")
            col.separator()
            
            # QUICK NAVIGATION (High frequency)
            col.label(text="Quick Navigation:")
            col.operator("view3d.view_all", text="Frame All Objects (Home)")
            col.operator("view3d.view_selected", text="Frame Selected (Numpad .)")
            col.operator("view3d.snap_cursor_to_center", text="Reset View Focus (Shift + C)")
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
            
            col.operator("view3d.view_persportho", text="Perspective/Orthographic Toggle (Numpad 5)")
            col.separator()
            
            # ADVANCED NAVIGATION
            col.label(text="Advanced Navigation:")
            col.operator("view3d.walk", text="Walk Mode (Shift + `)")
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
            
            # VIEWPORT SETTINGS (Less common but useful)
            col.separator()
            col.label(text="Viewport Settings:")
            if hasattr(context.preferences.inputs, 'use_mouse_emulate_3_button'):
                col.prop(context.preferences.inputs, "use_mouse_emulate_3_button", text="Emulate 3 Button Mouse")
            col.prop(context.preferences.view, "smooth_view", text="Smooth View Transitions")

        # 🧩 Transform and Manipulation
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_transform", text="Transform and Manipulation", emboss=False, icon='ORIENTATION_GIMBAL')
        if scene.show_transform:
            col = box.column(align=True)
            
            # THE WHY - What is Transform?
            col.label(text="Transform = Change Position, Rotation, Scale")
            col.label(text="Works in: Object Mode & Edit Mode")
            col.separator()
            
            # CORE TRANSFORMS (work everywhere)
            col.label(text="Basic Transforms:")
            row = col.row()
            row.scale_y = 1.2
            row.operator("transform.translate", text="Move (G)")
            row.operator("transform.rotate", text="Rotate (R)")
            row.operator("transform.resize", text="Scale (S)")
            
            # CONSTRAINT HELPERS
            col.label(text="Axis Constraints (after G/R/S):")
            col.label(text="• X-axis only: X • Y-axis only: Y • Z-axis only: Z")
            col.label(text="• Local axes: XX, YY, ZZ")
            col.separator()
            
            # EDIT MODE SPECIFIC
            col.label(text="Edit Mode - Create New Geometry:")
            col.operator("mesh.extrude_region_move", text="Extrude Faces/Edges (E)")
            col.operator("mesh.inset_faces", text="Inset Faces (I)")
            col.separator()
            
            # EDIT MODE SPECIFIC - Modify Existing
            col.label(text="Edit Mode - Modify Existing:")
            col.operator("mesh.bevel", text="Bevel Edges/Vertices (Ctrl+B)")
            col.operator("mesh.loopcut_slide", text="Add Loop Cut (Ctrl+R)")
            col.operator("mesh.shrink_fatten", text="Shrink/Fatten Along Normals (Alt+S)")
            col.separator()
            
            # VERTEX OPERATIONS
            col.label(text="Edit Mode - Vertex Tools:")
            col.operator("mesh.merge", text="Merge Vertices (M)")
            col.operator("mesh.rip_vertices", text="Rip Vertices (V)")
            col.operator("mesh.fill", text="Fill Faces (F)")
            col.separator()
            
            # ADVANCED HELPERS
            col.label(text="Advanced Options:")
            col.operator("transform.proportional_edit", text="Toggle Proportional Editing (O)")
            col.prop(context.tool_settings, "use_snap", text="Enable Snapping") 


        # 🧩 World Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_world_origin", text="World Origin", emboss=False, icon='ORIENTATION_GLOBAL')
        if scene.show_world_origin:
            col = box.column(align=True)
            
            # THE WHY - What is World Origin?
            col.label(text="World Origin = The Center of Your 3D Space")
            col.label(text="Located at coordinates (0,0,0)")
            col.label(text="Reference point for everything in your scene")
            col.separator()
            
            # NAVIGATION & VIEWING
            col.label(text="Navigation:")
            col.operator("view3d.view_all", text="Frame All Objects (Home)")
            col.operator("view3d.view_center_cursor", text="Center View on World Origin")
            col.label(text="• Frame All: See everything in your scene")
            col.label(text="• Center View: Focus on the world center")
            col.separator()
            
            # 3D CURSOR CONTROL
            col.label(text="3D Cursor (The Red & White Target):")
            col.operator("view3d.snap_cursor_to_center", text="Reset 3D Cursor to World Origin")
            col.label(text="• 3D Cursor marks where new objects appear")
            col.label(text="• Shift+Right-click to move cursor anywhere")
            col.separator()
            
            # MOVING OBJECTS TO WORLD ORIGIN
            col.label(text="Move Objects to World Origin:")
            col.operator("object.location_clear", text="Move Selected to World Origin").clear_delta = False
            col.operator("object.rotation_clear", text="Reset Selected Rotation").clear_delta = False
            col.operator("object.scale_clear", text="Reset Selected Scale").clear_delta = False
            col.label(text="• Location: Moves object to (0,0,0)")
            col.label(text="• Rotation: Straightens object")
            col.label(text="• Scale: Returns to original size")
            col.separator()
            
            # SHOWING ORIGINS IN VIEWPORT
            col.label(text="Show Reference Points:")
            col.prop(context.space_data.overlay, "show_object_origins", text="Show All Object Origins")
            col.prop(context.space_data.overlay, "show_cursor", text="Show 3D Cursor")
            col.label(text="• Orange dots = Object centers")
            col.label(text="• Red/white target = 3D cursor")

        # 🧩 Object Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_origin", text="Object Origin", emboss=False, icon='OBJECT_ORIGIN')
        if scene.show_object_origin:
            col = box.column(align=True)
            
            # Maybe add this at the start of Object Origin:
            col.label(text="Object Origin = Pivot Point for:")
            col.label(text="• Rotation • Scaling • Position")
            col.separator()
            
            # Add this at the top of Object Origin section:
            col.label(text="Show Origins in Viewport:")
            col.prop(context.space_data.overlay, "show_object_origins", text="Show All Object Origins")
            col.prop(context.space_data.overlay, "show_cursor", text="Show 3D Cursor")
            
            # Add these explanatory operations:
            col.label(text="Find & See Origins:")
            col.operator("view3d.view_selected", text="Focus View on Selected Object")
            col.operator("object.select_all", text="Select All Objects").action = 'SELECT'

            col.label(text="Origin Placement Options:")
            col.operator("object.origin_set", text="Origin to Center of Mass").type = 'ORIGIN_CENTER_OF_MASS'
            col.operator("object.origin_set", text="Origin to Bounding Box Center").type = 'ORIGIN_CENTER_OF_VOLUME'
            col.operator("object.origin_set", text="Origin to Bottom of Object").type = 'ORIGIN_GEOMETRY'

            # 3D Cursor ↔ Object Origin
            col.label(text="3D Cursor ↔ Object Origin:")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Object Origin")
            col.operator("view3d.snap_selected_to_cursor", text="Move Object to 3D Cursor").use_offset = False

            # Object Origin ↔ Object Geometry
            col.label(text="Object Origin ↔ Object Geometry:")
            col.operator("object.origin_set", text="Move Object Origin to Object Geometry").type = 'ORIGIN_GEOMETRY'
            col.operator("object.origin_set", text="Move Object Geometry to Object Origin").type = 'GEOMETRY_ORIGIN'

            # 3D Cursor ↔ Object Geometry
            col.label(text="3D Cursor ↔ Object Geometry:")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Object Geometry")
            col.operator("view3d.snap_selected_to_cursor", text="Move Object Geometry to 3D Cursor").use_offset = True

        # 🧩 3D Cursor
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_cursor", text="3D Cursor", emboss=False, icon='CURSOR')
        if scene.show_cursor:
            col = box.column(align=True)
            
            # THE WHY - What is the 3D Cursor?
            col.label(text="3D Cursor = Universal Reference Point")
            col.label(text="Use it to: Position • Snap • Create • Measure")
            col.separator()
            
            # Show the cursor visually
            col.prop(context.space_data.overlay, "show_cursor", text="Show 3D Cursor in Viewport")
            col.separator()
            
            # INVERSE PAIRS - clearly labeled
            col.label(text="Move TO Cursor ↔ Move FROM Cursor:")
            
            # Objects
            col.label(text="• Objects:")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="Cursor → Object")
            row.operator("view3d.snap_selected_to_cursor", text="Object → Cursor")
            
            # Vertices (Edit Mode)
            col.label(text="• Vertices (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="Cursor → Vertex")
            row.operator("view3d.snap_selected_to_cursor", text="Vertex → Cursor")
            
            # Edges (Edit Mode)
            col.label(text="• Edges (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="Cursor → Edge")
            row.operator("view3d.snap_selected_to_cursor", text="Edge → Cursor")
            
            # Faces (Edit Mode)
            col.label(text="• Faces (Edit Mode):")
            row = col.row()
            row.operator("view3d.snap_cursor_to_selected", text="Cursor → Face")
            row.operator("view3d.snap_selected_to_cursor", text="Face → Cursor")
            
            col.separator()
            
            # Reset option
            col.operator("view3d.snap_cursor_to_center", text="Reset Cursor to World Origin (0,0,0)")      


   

        # 🧩 Object Mode
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_mode", text="Object Mode", emboss=False, icon='OBJECT_DATAMODE')
        if scene.show_object_mode:
            col = box.column(align=True)
            
            # THE WHY - What is Object Mode?
            col.label(text="Object Mode = Work with Whole Objects")
            col.label(text="Move, copy, delete entire objects")
            col.separator()
            
            # SELECTION (Most Basic)
            col.label(text="Selection:")
            col.operator("object.select_all", text="Select All/Deselect All (A)")
            col.label(text="• Click object to select")
            col.label(text="• Shift+Click to select multiple")
            col.separator()
            
            # BASIC OBJECT OPERATIONS
            col.label(text="Basic Operations:")
            col.operator("object.duplicate_move", text="Duplicate (Shift + D)")
            col.operator("object.delete", text="Delete (X or Delete)")
            col.label(text="• Duplicate: Creates copy you can move")
            col.label(text="• Delete: Removes object completely")
            col.separator()
            
            # COMBINING OBJECTS
            col.label(text="Combine Objects:")
            col.operator("object.join", text="Join into One Object (Ctrl + J)")
            col.label(text="• Select multiple objects first")
            col.label(text="• Last selected becomes the result")
            col.separator()
            
            # ORGANIZATION
            col.label(text="Organization:")
            col.operator("object.move_to_collection", text="Move to Collection (M)")
            col.operator("object.hide_viewport", text="Hide Selected (H)")
            col.operator("object.hide_viewport_unselected", text="Unhide All (Alt + H)")
            col.label(text="• Collections = Folders for objects")
            col.separator()
            
            # APPEARANCE
            col.label(text="Surface Appearance:")
            col.operator("object.shade_smooth", text="Shade Smooth")
            col.operator("object.shade_flat", text="Shade Flat")
            col.label(text="• Smooth = Curved surfaces")
            col.label(text="• Flat = Angular surfaces")
            col.separator()
            
            # ADVANCED
            col.label(text="Advanced:")
            col.operator("object.transform_apply", text="Apply Transformations (Ctrl + A)")
            col.operator("object.origin_set", text="Set Origin to Geometry").type = 'ORIGIN_GEOMETRY'
            col.label(text="• Apply: Makes current size/rotation permanent")
            col.label(text="• Origin: Center point for rotations")

        # 🧩 Edit Mode  
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_edit_mode", text="Edit Mode", emboss=False, icon='EDITMODE_HLT')
        if scene.show_edit_mode:
            col = box.column(align=True)
            
            # THE WHY - What is Edit Mode?
            col.label(text="Edit Mode = Modify Object Shape")
            col.label(text="Work with vertices, edges, faces")
            col.label(text="Tab = Switch between Object/Edit Mode")
            col.separator()
            
            # SELECTION MODES
            col.label(text="Selection Modes:")
            col.label(text="• 1 = Vertex mode (points)")
            col.label(text="• 2 = Edge mode (lines)")  
            col.label(text="• 3 = Face mode (surfaces)")
            col.separator()
            
            # BASIC SELECTION
            col.label(text="Selection:")
            col.operator("mesh.select_all", text="Select All/None (A)")
            col.operator("mesh.select_linked", text="Select Connected (L)")
            col.operator("mesh.select_inverse", text="Select Opposite (Ctrl + I)")
            col.operator("mesh.select_more", text="Grow Selection (Ctrl + +)")
            col.operator("mesh.select_less", text="Shrink Selection (Ctrl + -)")
            col.separator()
            
            # ESSENTIAL MODELING TOOLS
            col.label(text="Essential Tools:")
            col.operator("mesh.extrude_region_move", text="Extrude (E)")
            col.label(text="• Extrude = Pull out new geometry")
            col.separator()
            
            col.operator("mesh.loopcut_slide", text="Loop Cut (Ctrl + R)")
            col.label(text="• Loop Cut = Add edge ring around object")
            col.separator()
            
            col.operator("mesh.inset_faces", text="Inset Faces (I)")
            col.label(text="• Inset = Create smaller face inside")
            col.separator()
            
            col.operator("mesh.bevel", text="Bevel (Ctrl + B)")
            col.label(text="• Bevel = Round off sharp edges")
            col.separator()
            
            # ADVANCED EXTRUDE OPTIONS
            col.label(text="Extrude Options (Alt + E):")
            col.operator("mesh.extrude_faces_move", text="Extrude Faces")
            col.operator("mesh.extrude_edges_move", text="Extrude Edges") 
            col.operator("mesh.extrude_vertices_move", text="Extrude Vertices")
            col.separator()
            
            # MESH CLEANUP
            col.label(text="Cleanup:")
            col.operator("mesh.merge", text="Merge Vertices (M)")
            col.operator("mesh.remove_doubles", text="Remove Duplicates")
            col.operator("mesh.fill", text="Fill Holes (F)")
            col.label(text="• Merge = Combine nearby vertices")
            col.label(text="• Fill = Close gaps in mesh")
            col.separator()
            
            # ADVANCED OPERATIONS
            col.label(text="Advanced:")
            col.operator("mesh.rip_vertices", text="Rip Vertices (V)")
            col.operator("mesh.shrink_fatten", text="Shrink/Fatten (Alt + S)")
            col.operator("mesh.separate", text="Separate Parts (P)")
            col.label(text="• Rip = Split vertices apart")
            col.label(text="• Shrink/Fatten = Move along normals")
            col.label(text="• Separate = Break into separate objects")
            
        # 🧩 Camera
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_camera", text="Camera", emboss=False, icon='CAMERA_DATA')
        if scene.show_camera:
            col = box.column(align=True)
            
            # THE WHY - What is a Camera?
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
            
            # CAMERA VIEWING
            col.label(text="Camera View:")
            col.operator("view3d.view_camera", text="Look Through Camera (Numpad 0)")
            col.label(text="• See exactly what will be rendered")
            col.separator()
            
            # CAMERA POSITIONING
            col.label(text="Position Camera:")
            col.operator("view3d.camera_to_view", text="Move Camera to Current View (Ctrl + Alt + Numpad 0)")
            col.label(text="• First: Navigate to desired view")
            col.label(text="• Then: Use this to position camera there")
            col.separator()
            
            # CAMERA LOCK (Advanced but Important)
            col.label(text="Camera Lock:")
            if hasattr(context.space_data, 'lock_camera'):
                col.prop(context.space_data, "lock_camera", text="Lock Camera to View")
                col.label(text="• When locked: Moving view = moving camera")
                col.label(text="• When unlocked: Camera stays put")
            col.separator()
            
            # CAMERA PROPERTIES
            col.label(text="Camera Settings:")
            if context.scene.camera and context.scene.camera.data:
                camera_data = context.scene.camera.data
                col.prop(camera_data, "lens", text="Focal Length (mm)")
                col.label(text="• Lower = Wider view (18mm = very wide)")
                col.label(text="• Higher = Narrower view (85mm = portrait)")
                col.separator()
                
                # Depth of Field toggle
                col.prop(camera_data.dof, "use_dof", text="Depth of Field (Blur)")
                if camera_data.dof.use_dof:
                    col.prop(camera_data.dof, "aperture_fstop", text="F-Stop (Blur Amount)")
                    col.prop(camera_data.dof, "focus_distance", text="Focus Distance")
            
            # CAMERA SELECTION
            col.separator()
            col.label(text="Camera Object:")
            col.operator("object.select_camera", text="Select Camera Object")
            col.label(text="• Select to move/rotate like any object")
            
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
                col.label(text="• Use multiple cameras for different shots")            

        # 🧩 Render
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_render", text="Render", emboss=False, icon='RENDER_STILL')
        if scene.show_render:
            col = box.column(align=True)
            
            # THE WHY - What is Rendering?
            col.label(text="Render = Create Final Image/Video")
            col.label(text="Converts 3D scene into 2D picture")
            col.separator()
            
            # RENDER ENGINE
            col.label(text="Render Engine:")
            col.prop(context.scene.render, "engine", text="")
            if context.scene.render.engine == 'BLENDER_EEVEE':
                col.label(text="• Eevee = Fast, good for previews")
            elif context.scene.render.engine == 'CYCLES':
                col.label(text="• Cycles = Slow, photorealistic")
            elif context.scene.render.engine == 'BLENDER_WORKBENCH':
                col.label(text="• Workbench = Very fast, simple")
            col.separator()
            
            # RENDER ACTIONS
            col.label(text="Render Actions:")
            col.operator("render.render", text="Render Image (F12)")
            col.operator("render.view_show", text="View Last Render (F11)")
            col.separator()
            
            # ANIMATION
            col.label(text="Animation:")
            col.operator("render.render", text="Render Animation (Ctrl + F12)").animation = True
            col.operator("render.play_rendered_anim", text="Play Rendered Animation")
            col.separator()
            
            # OUTPUT SETTINGS
            col.label(text="Output Settings:")
            col.prop(context.scene.render, "resolution_x", text="Width")
            col.prop(context.scene.render, "resolution_y", text="Height")
            col.prop(context.scene.render, "resolution_percentage", text="Quality %")
            col.label(text="• 100% = Full quality, 50% = Half size")
            col.separator()
            
            # FILE FORMAT
            col.label(text="File Format:")
            col.prop(context.scene.render.image_settings, "file_format", text="")
            col.prop(context.scene.render, "filepath", text="Save Location")
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
            
            # VIEWPORT RENDER
            col.label(text="Quick Preview:")
            col.operator("render.opengl", text="Viewport Render (Current View)")
            col.label(text="• Fast render of current viewport")
            col.separator()
            
            # RENDER REGION
            col.label(text="Partial Render:")
            col.operator("view3d.render_border", text="Set Render Border (Ctrl + B)")
            col.prop(context.scene.render, "use_border", text="Use Border")
            col.label(text="• Render only part of image (faster testing)")
            col.separator()
            
            # COMMON ISSUES
            col.label(text="Common Issues:")
            col.label(text="• Black render = No lights in scene")
            col.label(text="• Noisy render = Increase samples")
            col.label(text="• Slow render = Lower samples/resolution")
            col.separator()
            
            # LIGHTING CHECK
            lights_in_scene = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
            if not lights_in_scene and context.scene.render.engine != 'BLENDER_WORKBENCH':
                col.label(text="⚠ No Lights in Scene")
                col.operator("object.light_add", text="Add Light").type = 'SUN'
            else:
                col.label(text=f"✓ {len(lights_in_scene)} Light(s) in Scene")
            
            # MATERIAL CHECK
            if context.active_object and context.active_object.type == 'MESH':
                if not context.active_object.material_slots:
                    col.label(text="⚠ No Materials on Active Object")
                    col.operator("object.material_slot_add", text="Add Material Slot")
                else:
                    col.label(text="✓ Materials Present")
            
        # 🧩 About
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_about", text="About", emboss=False, icon='INFO')
        if scene.show_about:
            col = box.column(align=True)
            
            # HEADER WITH LOGO SPACE
            header_box = col.box()
            header_col = header_box.column(align=True)
            header_col.scale_y = 1.2
            header_col.label(text="🎯 BLENDER CHEATSHEETS", icon='COMMUNITY')
            header_col.label(text="Making Blender Accessible for Everyone")
            
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
            
            # VERSION INFO
            version_box = col.box()
            version_col = version_box.column(align=True)
            version_col.label(text="🔧 Version Info:")
            version_col.label(text="• Designed for Blender 3.6+ LTS")
            version_col.label(text="• Focus on core modeling essentials")
            version_col.label(text="• Free for life under GPLv2")
            version_col.label(text="• Regular updates for LTS versions")
            
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
            
            # INSPIRATIONAL FOOTER
            footer_box = col.box()
            footer_col = footer_box.column(align=True)
            footer_col.scale_y = 0.8
            footer_col.label(text="🚀 'Enjoy using Blender with new eyes'")
            footer_col.label(text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            footer_col.label(text="Making complex software simple, one tool at a time.")
            
            # VERSION/BUILD INFO (Optional)
            col.separator()
            info_col = col.column(align=True)
            info_col.scale_y = 0.7
            info_col.label(text="Build: v1.0 | License: GPLv2 | Community Driven")
            

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
    SHORTCUTS_OT_ObjectMode,
    SHORTCUTS_OT_EditMode,
)

def register():
    register_properties()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    unregister_properties()

if __name__ == "__main__":
    register()
