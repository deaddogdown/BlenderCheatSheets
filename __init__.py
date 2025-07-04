bl_info = {
    "name": "CheatSheets",
    "author": "Dead Dog Down - Game Studio",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "3D View > N-Panel > CheatSheets",
    "description": "Quick access to commonly used Blender shortcuts in collapsible sections.",
    "category": "Accessibility"
}

if "bpy" in locals():
    import importlib
    importlib.reload(blenderCheatSheets)
else:
    from . import blenderCheatSheets

import bpy

def register():
    blenderCheatSheets.register()

def unregister():
    blenderCheatSheets.unregister()

if __name__ == "__main__":
    register()
