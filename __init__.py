bl_info = {
    "name": "ORTS Collection Tools",
    "author": "Pete Willard",
    "version": (1, 2),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Collection Tools Tab",
    "description": "Swap collection names and create structured collection setups with icons and auto-refresh",
    "category": "Object",
}

import bpy
import os
import bpy.utils.previews
from . import ORTSCollection

preview_collections = {}

def register_icons():
    global preview_collections
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    pcoll = bpy.utils.previews.new()
    icon_path = os.path.join(icons_dir, "collection_tools_icon.png")
    if os.path.exists(icon_path):
        pcoll.load("collection_tools_icon", icon_path, 'IMAGE')
    preview_collections["main"] = pcoll
    bpy.types.WindowManager.orts_icons = pcoll

def unregister_icons():
    global preview_collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    if hasattr(bpy.types.WindowManager, "orts_icons"):
        del bpy.types.WindowManager.orts_icons

def register():
    register_icons()
    ORTSCollection.register()

def unregister():
    ORTSCollection.unregister()
    unregister_icons()

if __name__ == "__main__":
    register()
