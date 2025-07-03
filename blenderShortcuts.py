import bpy

# Register collapsible section properties
def register_properties():
    props = [
        ('show_general', False),
        ('show_view', False),
        ('show_world_origin', False),
        ('show_object_origin', False),
        ('show_cursor', False),
        ('show_transform', False),
        ('show_navigation', False),
        ('show_camera', False),
        ('show_object_mode', False),
        ('show_edit_mode', False),
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
        'show_view',
        'show_world_origin',
        'show_object_origin',
        'show_cursor',
        'show_transform',
        'show_navigation',
        'show_camera',
        'show_object_mode',
        'show_edit_mode',
        'show_render',
        'show_about'
    ]
    for prop in props:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)

class SHORTCUTS_PT_Panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender Shortcuts"
    bl_label = "Blender Shortcuts"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 🧩 General
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_general", text="General", emboss=False, icon='INFO')
        if scene.show_general:
            col = box.column(align=True)
            col.operator("wm.search_menu", text="Search Operators: F3 or Spacebar")
            col.operator("wm.undo", text="Undo: Ctrl + Z")
            col.operator("wm.redo", text="Redo: Ctrl + Shift + Z")
            col.operator("wm.copy_data_path_button", text="Copy: Ctrl + C")
            col.operator("wm.paste_data_path_button", text="Paste: Ctrl + V")
            col.operator("object.duplicate_move", text="Duplicate: Shift + D")
            col.operator("object.make_single_user", text="Make Unique: U")
        
        # 🧩 View
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_view", text="View", emboss=False, icon='VIEW_CAMERA')
        if scene.show_view:
            col = box.column(align=True)
            col.label(text="Mouse:")
            col.operator("view3d.view_orbit", text="Orbit View: Middle Mouse Button (MMB) Drag")
            col.operator("view3d.view_pan", text="Pan View: Shift + MMB Drag")
            col.operator("view3d.view_zoom", text="Zoom In/Out: Scroll Wheel or Ctrl + MMB Drag")
            col.label(text="Numpad:")
            col.operator("view3d.view_axis", text="Top View: Numpad 7").type = 'TOP'
            col.operator("view3d.view_axis", text="Front View: Numpad 1").type = 'FRONT'
            col.operator("view3d.view_axis", text="Right View: Numpad 3").type = 'RIGHT'
            col.operator("view3d.view_axis", text="Bottom View: Ctrl + Numpad 7").type = 'BOTTOM'
            col.operator("view3d.view_axis", text="Back View: Ctrl + Numpad 1").type = 'BACK'
            col.operator("view3d.view_axis", text="Left View: Ctrl + Numpad 3").type = 'LEFT'
            col.operator("view3d.view_persportho", text="Perspective/Orthographic Toggle: Numpad 5")
            col.label(text="Keyboard:")
            col.operator("view3d.snap_cursor_to_center", text="Reset View: Shift + C")
            col.operator("view3d.view_all", text="Frame All: Home")
            col.operator("view3d.view_selected", text="Frame Selected: Numpad .")
            col.operator("view3d.walk", text="Fly/Walk Mode: Shift + ` or Shift + F")
            col.operator("view3d.camera_to_view", text="Align Active Camera to View: Ctrl + Alt + Numpad 0")
            col.operator("wm.empty_operator", text="Lock Camera to View: N → Lock Camera to View")
            col.operator("wm.empty_operator", text="Move Camera with View (When Locked): Shift + MMB (Pan), Scroll Wheel (Zoom)")
            col.operator("wm.empty_operator", text="Dolly Camera In/Out: Ctrl + Shift + MMB Drag")
            col.operator("camera.focus_set", text="Camera Focal Length Adjustment: Ctrl + F")


        # 🧩 World Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_world_origin", text="World Origin", emboss=False, icon='ORIENTATION_GLOBAL')
        if scene.show_world_origin:
            col = box.column(align=True)
            col.operator("view3d.snap_cursor_to_center", text="Move 3D Cursor to World Origin")
            col.operator("object.location_clear", text="Move Selected to World Origin").clear_delta = False

        # 🧩 Object Origin
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_origin", text="Object Origin", emboss=False, icon='OBJECT_ORIGIN')
        if scene.show_object_origin:
            col = box.column(align=True)

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

        # 🧩 Cursor
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_cursor", text="3D Cursor", emboss=False, icon='MOUSE_MOVE')
        if scene.show_cursor:
            col = box.column(align=True)

            # Object Origin ↔ Object Geometry
            col.label(text="Object Origin ↔ Object Geometry")
            col.operator("object.origin_set", text="Move Object Origin to Object Geometry").type = 'ORIGIN_GEOMETRY'
            col.operator("object.origin_set", text="Move Object Geometry to Object Origin").type = 'GEOMETRY_ORIGIN'

            # Object ↔ 3D Cursor
            col.label(text="Object ↔ 3D Cursor")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Selected Object")
            col.operator("view3d.snap_selected_to_cursor", text="Move Selected Object to 3D Cursor")

            # Vertex ↔ 3D Cursor
            col.label(text="Vertex ↔ 3D Cursor")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Selected Vertex")
            col.operator("view3d.snap_selected_to_cursor", text="Move Selected Vertex to 3D Cursor")

            # Edge ↔ 3D Cursor
            col.label(text="Edge ↔ 3D Cursor")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Selected Edge")
            col.operator("view3d.snap_selected_to_cursor", text="Move Selected Edge to 3D Cursor")

            # Face ↔ 3D Cursor
            col.label(text="Face ↔ 3D Cursor")
            col.operator("view3d.snap_cursor_to_selected", text="Move 3D Cursor to Selected Face")
            col.operator("view3d.snap_selected_to_cursor", text="Move Selected Face to 3D Cursor")       


        # 🧩 Transform and Manipulation
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_transform", text="Transform and Manipulation", emboss=False, icon='VIEW_PERSPECTIVE')
        if scene.show_transform:
            col = box.column(align=True)

            # Basic Transformations
            col.label(text="Basic Transformations:")
            col.operator("transform.translate", text="Move (Grab): G")
            col.operator("transform.rotate", text="Rotate: R")
            col.operator("transform.resize", text="Scale: S")
            col.operator("transform.proportional_edit", text="Proportional Editing: O")

            # Mesh Extrusion & Inset
            col.label(text="Mesh Extrusion & Inset:")
            col.operator("mesh.extrude_region_move", text="Extrude: E")
            col.operator("mesh.inset_faces", text="Inset Faces: I")

            # Bevel & Loop Cut
            col.label(text="Bevel & Loop Cut:")
            col.operator("mesh.bevel", text="Bevel: Ctrl + B")
            col.operator("mesh.loopcut_slide", text="Loop Cut: Ctrl + R")

            # Vertex Operations
            col.label(text="Vertex Operations:")
            col.operator("mesh.merge", text="Merge Vertices: M")
            col.operator("mesh.rip_vertices", text="Rip Vertices: V")
            col.operator("mesh.shrink_fatten", text="Shrink/Fatten: Alt + S")

            # Face/Edge Tools
            col.label(text="Face/Edge Tools:")
            col.operator("mesh.fill", text="Fill Faces: F")     

        # 🧩 Navigation
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_navigation", text="Navigation", emboss=False, icon='VIEW_CAMERA')
        if scene.show_navigation:
            col = box.column(align=True)
            
            # Core Navigation Actions
            col.label(text="Mouse:")
            col.operator("wm.empty_operator", text="Orbit View: Middle Mouse Button (MMB) Drag")
            col.operator("wm.empty_operator", text="Pan View: Shift + MMB Drag")
            col.operator("wm.empty_operator", text="Zoom In/Out: Scroll Wheel or Ctrl + MMB Drag")

            # Fly/Walk Mode
            col.label(text="Keyboard:")
            col.operator("view3d.walk", text="Fly/Walk Mode: Shift + ` or Shift + F")

        # 🧩 Camera (Object)
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_camera", text="Camera Object", emboss=False, icon='CAMERA_DATA')
        if scene.show_camera:
            col = box.column(align=True)
    
            # Switch to Camera View
            col.operator("view3d.view_camera", text="View ↔ Camera: Numpad 0")

            # Align Active Camera to View
            col.operator("camera.set_active", text="Move Active Camera to View: Ctrl + Alt + Numpad 0")

            # Lock Camera to View
            col.operator("screen.lock_camera", text="Lock Camera to View: N → Lock Camera to View")

            # Move Camera with View (When Locked)
            col.operator("view3d.view_selected", text="Move Camera with View (When Locked): Shift + MMB (Pan), Scroll Wheel (Zoom)")

            # Dolly Camera In/Out
            col.operator("view3d.view_selected", text="Dolly Camera In/Out: Ctrl + Shift + MMB Drag")

            # Adjust Camera Focal Length
            col.operator("camera.focal_length_set", text="Adjust Camera Focal Length: Ctrl + F")

        # 🧩 Object Mode
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_object_mode", text="Object Mode", emboss=False, icon='OBJECT_DATAMODE')
        if scene.show_object_mode:
            col = box.column(align=True)

            # Selection
            col.operator("object.select_all", text="Select All/Deselect All: A")

            # Duplicate
            col.operator("object.duplicate_move", text="Duplicate: Shift + D")

            # Delete
            col.operator("object.delete", text="Delete Object: X or Delete")

            # Join
            col.operator("object.join", text="Join Objects: Ctrl + J")

            # Separate
            col.operator("object.separate", text="Separate by Selection/Material/Loose Parts: P")

            

            # Move to Layer (Collection)
            col.operator("object.move_to_collection", text="Move Object to Collection: M")

            # Apply Transformation
            col.operator("object.transform_apply", text="Apply Transformation: Ctrl + A")

            # Hide/Unhide
            col.operator("object.hide_viewport", text="Hide Selected: H")
            col.operator("object.hide_viewport_unselected", text="Unhide All: Alt + H")

            # Origin
            col.operator("object.origin_set", text="Move Origin to Geometry: Ctrl + Shift + Alt + C").type = 'ORIGIN_GEOMETRY'
            
            col.label(text="Shade:")
            # Shade Smooth/Flat
            col.operator("object.shade_smooth", text="Shade Smooth: W")
            col.operator("object.shade_flat", text="Shade Flat: W")

        # 🧩 Edit Mode
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_edit_mode", text="Edit Mode", emboss=False, icon='EDITMODE_HLT')
        if scene.show_edit_mode:
            col = box.column(align=True)

            # Basic Selection Tools
            col.label(text="Selection:")
            col.operator("mesh.select_all", text="Select All/Deselect All: A")
            col.operator("mesh.select_linked", text="Select Linked: L")
            col.operator("mesh.select_inverse", text="Select Inverse: Ctrl + I")

            # Extrusion & Inset
            col.label(text="Extrusion & Inset:")
            col.operator("mesh.extrude_region_move", text="Extrude: E")
            col.operator("mesh.inset_faces", text="Inset Faces: I")

            # Bevel & Loop Cut
            col.label(text="Bevel & Loop Cut:")
            col.operator("mesh.bevel", text="Bevel: Ctrl + B")
            col.operator("mesh.loopcut_slide", text="Loop Cut and Slide: Ctrl + R")

            # Merge & Rip
            col.label(text="Merge & Rip:")
            col.operator("mesh.merge", text="Merge Vertices: M")
            col.operator("mesh.rip_vertices", text="Rip Vertices: V")

            # Shrink/Fatten & Fill
            col.label(text="Shrink/Fatten & Fill:")
            col.operator("mesh.shrink_fatten", text="Shrink/Fatten: Alt + S")
            col.operator("mesh.fill", text="Fill Faces: F")

            # Select More/Less
            col.label(text="Select More/Less:")
            col.operator("mesh.select_more", text="Select More: Ctrl + Numpad +")
            col.operator("mesh.select_less", text="Select Less: Ctrl + Numpad -")

        # 🧩 Render
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_render", text="Render", emboss=False, icon='RENDER_STILL')
        if scene.show_render:
            col = box.column(align=True)
            col.label(text="Render:")
            col.operator("render.render", text="Render Image: F12")
            col.operator("render.render", text="Render Animation: Ctrl + F12").animation = True
            col.operator("image.open", text="View Image: F11")
            col.operator("render.opengl", text="View Animation: Ctrl + F11")
            
        # 🧩 About
        box = layout.box()
        row = box.row()
        row.prop(scene, "show_about", text="About", emboss=False, icon='INFO')
        if scene.show_about:
            col = box.column(align=True)
            col.label(text="Welcome to Blender Shortcuts:")
            col.label(text="=====")
            col.label(text="This tool was designed to help")
            col.label(text="Modellers of all age ranges")
            col.label(text="see and access Blenders common")
            col.label(text="functions in an easy to use toolbar.")
            col.label(text="Transparent and easily accessible")
            col.label(text="even for Newbies, with standard")
            col.label(text="terminology and accessibility")
            col.label(text="to the most common keyboard,")
            col.label(text="mouse and numpad controls.")
            col.label(text="=====")
            col.label(text="Blender Shortcuts is free for life")
            col.label(text="and if you would like to support us")
            col.label(text="so we can keep this addon up-to-date")
            col.label(text="please feel free to donate, sponsor")
            col.label(text="and help fund this addon.")
            col.label(text="=====")
            col.label(text="Blender Shortcuts will only be")
            col.label(text="for LTS versions.")
            col.label(text="=====")
            col.label(text="Enjoy using Blender with new eyes")
            col.label(text="=====")
            col.label(text="DEAD DOG DOWN - GAME STUDIO")
            col.label(text="=====")
            col.label(text="Funders welcome via email")
            col.label(text="deaddogdown.gamestudio@gmail.com")

classes = (
    SHORTCUTS_PT_Panel,
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
