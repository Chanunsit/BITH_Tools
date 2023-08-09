import typing
import bpy

from . import G_Modul

from bpy.types import Menu, Operator, Panel
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)

# try:
#     bpy.ops.object.export_location(action="load")
#     # exportLocalList = G_Modul.string_to_list(context.scene.g_tools.ExportLocalList)
    
# except:
exportLocalList = []

class VIEW3D_PT_BatchExport(Panel):
    bl_label = "Export Path"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        if scene.FBXExportFolder is not None:
            row = layout.row()
            row.prop(scene, 'FBXExportFolder',)
            
            row = layout.row()
           
            row.operator("object.export_location", text="Load", icon="DISC").action = "load"
            row.operator("object.export_location", text="Save", icon="SOLO_ON").action = "save"
            global exportLocalList
            if exportLocalList is not None and exportLocalList != []:
                box = layout.box()
                for i in range(len(exportLocalList)):
                    row = box.row()
                    loc = exportLocalList[i].split("\\")
                    loc = "..." + loc[-3] + " \\ "  + loc[-2]
                    row.label(text=loc)
                    bt = row.operator("object.export_location", text="", icon="FOLDER_REDIRECT")
                    bt.action = "set"
                    bt.index = i
                    bt = row.operator("object.export_location", text="", icon="TRASH")
                    bt.action = "delete"
                    bt.index = i
        else:
            row = layout.row()
            row.label(text="Request Enfusion Blender Tools")
                

def minimizeLoc(loc):
    loc = loc.split("\\")
    loc = "..." + loc[-3] + " \\ "  + loc[-2]
    return loc

def locUpdate(self, context):
    items = [(loc, minimizeLoc(loc), "") for i, loc in enumerate(exportLocalList)]
    #self.location = items[0][0] if items else ""
    return items

class ExportLocation(Operator):
    bl_idname = "object.export_location"
    bl_label = "Export Location"

    action : StringProperty(name="Action")
    index : IntProperty(name="Index")
   
    location : EnumProperty(
        name="Property",
        items=locUpdate,
        update=locUpdate  # Add the update function
    )

    def execute(self, context):
        action = self.action
        if action == "save":
            self.save(self, context)
        elif action == "load":
            self.load(self, context)
        elif action == "delete":
            self.delete(self, context)
        elif action == "set":
            self.set(self, context)
        elif action == "export to":
            try:
                scene = context.scene
                scene.FBXExportFolder = self.location
                bpy.ops.collection.batch_export_fbx()
                G_Modul.refresh_panel()
            except:
                self.report({"INFO"} ,"Request Enfusion Blender Tools")
        return {'FINISHED'}
    @staticmethod
    def save(self, context):
        scene = context.scene
        if scene.FBXExportFolder != "":
            global exportLocalList
            exportLocalList.append(scene.FBXExportFolder)
            scene.g_tools.ExportLocalList = G_Modul.list_to_string(exportLocalList)
            # G_Modul.saveJsonFile(exportLocalList, "exportLocalList", "resources")
        else:
            self.report({"INFO"} ,"Please Select Path")
        return {'FINISHED'}
    @staticmethod
    def load(self, context):
        global exportLocalList
        exportLocalList = G_Modul.string_to_list(context.scene.g_tools.ExportLocalList)
        return {'FINISHED'}
    @staticmethod
    def delete(self, context):
        for i in range(len(exportLocalList)):
            if i == self.index:
                exportLocalList.pop(i)
        context.scene.g_tools.ExportLocalList = G_Modul.list_to_string(exportLocalList)
        return {'FINISHED'}
    @staticmethod
    def set(self, context):
        scene = context.scene
        scene.FBXExportFolder = exportLocalList[self.index]
        return {'FINISHED'}

def export_location(self, context):
    scene = context.scene
    if scene.FBXExportFolder is not None:
        self.layout.operator_menu_enum("object.export_location", property="location", text = "Export FBX to ").action = "export to"


def register():
    
    bpy.utils.register_class(VIEW3D_PT_BatchExport)
    bpy.utils.register_class(ExportLocation)
    bpy.types.OUTLINER_MT_collection.prepend(export_location)



def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_BatchExport)
    bpy.utils.unregister_class(ExportLocation)
    bpy.types.OUTLINER_MT_collection.remove(export_location)