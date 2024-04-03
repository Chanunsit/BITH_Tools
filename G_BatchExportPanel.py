import typing
import bpy

import re
import os

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
                # Check if the collection name contains 'dbr' and then set 'ExportSceneHierarchy' to 1 in the meta file
                self.report({'INFO'}, f"Export completed successfully: {context.collection.name}")                
                if 'dbr' in context.collection.name:
                    self.report({'INFO'}, 'dbr detected in collection name')
                    # Get the directory of scene.FBXExportFolder
                    export_folder = os.path.dirname(scene.FBXExportFolder)

                    # Check if .xob.meta file exists in the directory
                    meta_file_path = os.path.join(export_folder, context.collection.name + ".xob.meta")
                    if os.path.isfile(meta_file_path):
                        self.report({'INFO'}, 'Meta file detected')
                        # Open the meta file
                        with open(meta_file_path, 'r') as meta_file:
                            content = meta_file.read()
                            if "ExportSceneHierarchy" not in content:
                                content = re.sub(r'FBXResourceClass PC {', r'FBXResourceClass PC {\n    ExportSceneHierarchy 1', content)
                                # Write the modified content back to the meta file
                                with open(meta_file_path, 'w') as modified_meta_file:
                                    modified_meta_file.write(content)
                                    self.report({'INFO'}, 'ExportSceneHierarchy set to 1')
                                    if "ExportSceneHierarchy" not in content:
                                        self.report({'WARNING'}, "'ExportSceneHierarchy' not set 1 in meta file")
                            else:
                                self.report({'INFO'}, 'ExportSceneHierarchy already set to 1')            
                else:
                    self.report({'INFO'}, 'Meta file not detected')
                #--------------------------------------------------------------------------------------------------------------------
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