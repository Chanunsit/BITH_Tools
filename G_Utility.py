import bpy
from . import G_Modul

class AssignShareMat(bpy.types.Operator):
    bl_idname = "object.assign_share_material"
    bl_label = "Assign Share Material"

    index : bpy.props.StringProperty(name="Index")

    def execute(self, context):
        index = self.index
        activeObject = bpy.context.active_object
        activeObject.data.materials.clear()
        mat = G_Modul.create_material(index)
        activeObject.data.materials.append(mat)
        mat.use_nodes = True

        return {'FINISHED'}
    


def register():
    bpy.utils.register_class(AssignShareMat)

    
   
    
    
    

def unregister():
    bpy.utils.unregister_class(AssignShareMat)
