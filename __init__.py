bl_info = {
    "name": "Blender Shortcuts",
    "author": "Lee Franken",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "3D View > N-Panel > Blender Shortcuts",
    "description": "Quick access to commonly used Blender shortcuts in collapsible sections.",
    "category": "Interface"
}

if "bpy" in locals():
    import importlib
    importlib.reload(blenderShortcuts)
else:
    from . import blenderShortcuts

import bpy

def register():
    blenderShortcuts.register()

def unregister():
    blenderShortcuts.unregister()

if __name__ == "__main__":
    register()
