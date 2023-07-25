import bpy

from . import G_Modul

from bpy.types import Panel
from bpy.types import Operator

class OBJECT_OT_LODAnalyze(Operator):
    bl_idname = "object.lod_analyze"
    bl_label = "Analyze"

    action : bpy.props.StringProperty(name="Action")
    index : bpy.props.IntProperty(name="Index")

    def execute(self, context):
        if self.action == "analyze":
            self.analyze(self, context)
        elif self.action == "isolate":
            self.isolate(self, context)
        return {'FINISHED'}
    
    @staticmethod
    def analyze(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        lodList = G_Modul.find_lod(G_Modul.get_object_name())
        g_tools.report_lod = G_Modul.list_to_string(lodList)
        print(lodList)
        bpy.context.area.ui_type = 'OUTLINER'
        bpy.ops.outliner.select_all()
        bpy.ops.outliner.unhide_all()
        bpy.context.area.ui_type = 'VIEW_3D'
        triList = []
        for i in range(len(lodList)):
            bpy.ops.object.select_all(action='DESELECT')
            G_Modul.select_objects_by_name(lodList[i])
            triList.append(G_Modul.triangle_call())
        g_tools.report_tri = G_Modul.list_to_string(triList)            
        print(g_tools.report_tri)
        return {'FINISHED'}
    
    @staticmethod
    def isolate(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        lodList = G_Modul.find_lod(G_Modul.get_object_name())
        bpy.context.area.ui_type = 'OUTLINER'
        bpy.ops.outliner.select_all()
        bpy.ops.outliner.unhide_all()
        bpy.context.area.ui_type = 'VIEW_3D'
        G_Modul.select_objects_by_name(lodList[self.index])
        G_Modul.focus_object_in_outliner()
        bpy.ops.object.hide_view_set(unselected=True)
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_LODAnalyze)

   
    
    
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_LODAnalyze)
