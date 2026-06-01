bl_info = {
    "name": "CheatSheets",
    "author": "Dead Dog Down - Game Studio",
    "version": (1, 0, 1),
    "blender": (4, 5, 0),
    "location": "3D View > N-Panel > CheatSheets",
    "description": "Quick access to commonly used Blender shortcuts in collapsible sections.",
    "category": "Accessibility"
}

if "bpy" in locals():
    import importlib
    importlib.reload(blenderCheatSheets)
    importlib.reload(blenderCheatSheetsHelpers)  # Add this line
else:
    from . import blenderCheatSheets
    from . import blenderCheatSheetsHelpers      # Add this line

import bpy

def register():
    blenderCheatSheets.register()
    blenderCheatSheetsHelpers.register()         # Add this line

def unregister():
    blenderCheatSheets.unregister()
    blenderCheatSheetsHelpers.unregister()       # Add this line

if __name__ == "__main__":
    register()
