import bpy

def get_collections(self, context):
    items = [(coll.name, coll.name, "") for coll in bpy.data.collections]
    if not items:
        items = [("None", "None", "No collections available")]
    return items


class SwapCollectionsProperties(bpy.types.PropertyGroup):
    collection_1: bpy.props.EnumProperty(
        name="Collection 1",
        description="First collection to swap",
        items=get_collections,
    )
    collection_2: bpy.props.EnumProperty(
        name="Collection 2",
        description="Second collection to swap",
        items=get_collections,
    )


class OBJECT_OT_SwapCollections(bpy.types.Operator):
    bl_idname = "object.swap_collections"
    bl_label = "Swap Collection Names"
    bl_description = "Swap the names of two selected collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.swap_collections_props
        name1 = props.collection_1
        name2 = props.collection_2

        if name1 == "None" or name2 == "None":
            self.report({'ERROR'}, "No valid collections selected.")
            return {'CANCELLED'}

        if name1 == name2:
            self.report({'ERROR'}, "Cannot swap a collection with itself!")
            return {'CANCELLED'}

        coll1 = bpy.data.collections.get(name1)
        coll2 = bpy.data.collections.get(name2)

        if not coll1 or not coll2:
            self.report({'ERROR'}, "One or both collections not found.")
            return {'CANCELLED'}

        temp_name = coll1.name + "_TEMP"
        coll1.name = temp_name
        coll2.name = name1
        coll1.name = name2

        self.report({'INFO'}, f"Swapped '{name1}' ↔ '{name2}' successfully!")
        return {'FINISHED'}


class OBJECT_OT_CreateInitialCollections(bpy.types.Operator):
    bl_idname = "object.create_initial_collections"
    bl_label = "Create Initial Collection Setup"
    bl_description = "Create a default collection structure (MAIN & Scratchpad) with unique subcollections"
    bl_options = {'REGISTER', 'UNDO'}

    def create_collection(self, name, parent_collection=None):
        if name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(name)
            if parent_collection:
                parent_collection.children.link(new_collection)
            else:
                bpy.context.scene.collection.children.link(new_collection)
            return new_collection, True
        else:
            return bpy.data.collections[name], False

    def execute(self, context):
        created = []

        # MAIN and subcollections
        main, main_created = self.create_collection("MAIN")
        if main_created:
            created.append("MAIN")

        main_700, c1 = self.create_collection("MAIN_700", parent_collection=main)
        if c1:
            created.append("MAIN_700")

        main_2000, c2 = self.create_collection("MAIN_2000", parent_collection=main)
        if c2:
            created.append("MAIN_2000")

        # Scratchpad and independent subcollections
        scratchpad, s_created = self.create_collection("Scratchpad")
        if s_created:
            created.append("Scratchpad")

        scratchpad_700, c3 = self.create_collection("Scratchpad_700", parent_collection=scratchpad)
        if c3:
            created.append("Scratchpad_700")

        scratchpad_2000, c4 = self.create_collection("Scratchpad_2000", parent_collection=scratchpad)
        if c4:
            created.append("Scratchpad_2000")

        if not created:
            self.report({'INFO'}, "All collections already exist — nothing to do.")
        else:
            self.report({'INFO'}, f"Created collections: {', '.join(created)}")

        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()

        return {'FINISHED'}


class VIEW3D_PT_SwapCollections(bpy.types.Panel):
    bl_label = "Collection Tools"
    bl_idname = "VIEW3D_PT_swap_collections"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Collection Tools'

    def draw(self, context):
        layout = self.layout
        props = context.scene.swap_collections_props
        icons = getattr(bpy.context.window_manager, "orts_icons", None)
        icon_value = icons["collection_tools_icon"].icon_id if icons else 0

        layout.label(text="Initial Setup:")
        layout.operator("object.create_initial_collections", icon_value=icon_value)

        layout.separator()
        layout.label(text="Swap Collection Names:")
        layout.prop(props, "collection_1")
        layout.prop(props, "collection_2")
        layout.operator("object.swap_collections", icon_value=icon_value)


def refresh_panel(scene):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


classes = (
    SwapCollectionsProperties,
    OBJECT_OT_SwapCollections,
    OBJECT_OT_CreateInitialCollections,
    VIEW3D_PT_SwapCollections,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.swap_collections_props = bpy.props.PointerProperty(type=SwapCollectionsProperties)
    bpy.app.handlers.depsgraph_update_post.append(refresh_panel)

def unregister():
    if refresh_panel in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(refresh_panel)
    del bpy.types.Scene.swap_collections_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
