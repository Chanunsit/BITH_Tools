import bpy

class VIEW3D_PT_BatchExport(bpy.types.Panel):
    bl_label = "Export Path"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.prop(scene, 'FBXExportFolder',)

def register():
    bpy.utils.register_class(VIEW3D_PT_BatchExport)



def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_BatchExport)