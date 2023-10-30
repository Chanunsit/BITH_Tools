import bpy

from . import G_Modul
from . import G_Icon_reg
from . import G_Property


from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)


matDirList = []
matDirList = G_Modul.loadJsonFile("mat_folders", "resources")


editDirBool = False
editDir = ""
editDirIndex = 0

class VIEW3D_PT_CustomMaterial(bpy.types.Panel):
    bl_label = "Custom Material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'
    
    @classmethod
    def poll(cls, context):
        return context.scene.g_tools.custom_mat_panel and context.scene.g_tools.toolTab == "UTIL"
    
    def draw(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        
        layout = self.layout
        row = layout.row()
        row.label(text="Directories")
        row.operator("object.custom_materials", text="Load").action = "load"
        row.operator("object.custom_materials", text="", icon="ADD").action = "add"
        row = layout.row()
        if matDirList is not None:
            for i in range(len(matDirList)):
                dirName = matDirList[i].split("\\")               
                dirName = dirName[-2]
                if matDirList[i] == editDir and editDirIndex == i and editDirBool:
                    row.prop(g_tools, "mat_folder", text="")
                    bt = row.operator("object.custom_materials", text="", icon="CHECKMARK")
                    bt.action = "yes"
                    bt.index = i
                else:
                    row.label(text=dirName, icon="FILE_FOLDER")
                    bt = row.operator("object.custom_materials", text="", icon="OUTLINER_DATA_GP_LAYER")
                    bt.action = "edit"
                    bt.index = i
                    bt.dirIndex = matDirList[i]
                    bt = row.operator("object.custom_materials", text="", icon="X")
                    bt.action = "remove"
                    bt.index = i
                row = layout.row()

class CustomMaterial(bpy.types.Operator):
    bl_idname = "object.custom_materials"
    bl_label = "Custom Material"
    
    action : StringProperty(name="Action")
    index : IntProperty(name="Index")
    dirIndex : StringProperty(name="Index")
     
    def execute(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        if self.action == "load":
            self.load(self, context)
        elif self.action == "set":
            self.set(self, context)
        elif self.action == "add":
            self.add(self, context)
        elif self.action == "remove":
            self.remove(self, context)
        elif self.action == "edit":
            self.edit(self, context)
        elif self.action == "yes":
            self.yes(self, context)
        return {'FINISHED'}
    @staticmethod
    def load(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        print(matDirList)
        matName = []
        for i in range(len(matDirList)):
            matFiles = G_Modul.find_meta_files(matDirList[i])
            if matFiles is not None:
                for path in matFiles:
                    matFile = G_Modul.read_meta_file(path)
                    id, name = G_Modul.get_meta(matFile)
                    mat = []
                    name = name.split("/")
                    name = name[-1].split(".")
                    name = name[0]
                    mat.append(name + "_" + id)
                    mat.append(name)
                    matName.append(mat)
        print(matName)
        G_Modul.saveJsonFile(matName, "custom_mat", "resources")
        
        return {'FINISHED'}
    
    @staticmethod
    def set(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        print(g_tools.cusMat.items)
        return {'FINISHED'}
    
    @staticmethod
    def add(self, context):
        global matDirList
        scene = context.scene
        g_tools = scene.g_tools
        mat_dir = g_tools.mat_folder
        if g_tools.mat_folder != "":
            matDirList.append(mat_dir)
        else:
            g_tools.mat_folder = "C:\\"
            matDirList.append(g_tools.mat_folder)
        G_Modul.saveJsonFile(matDirList, "mat_folders", "resources")
        return {'FINISHED'}
    
    @staticmethod
    def remove(self, context):
        global matDirList
        scene = context.scene
        g_tools = scene.g_tools
        for i in range(len(matDirList)):
            if i == self.index:
                matDirList.pop(i)
        G_Modul.saveJsonFile(matDirList, "mat_folders", "resources")
        return {'FINISHED'}
    
    @staticmethod
    def edit(self, context):
        global editDir, editDirIndex, editDirBool
        editDir = self.dirIndex
        editDirIndex = self.index
        editDirBool = True
        scene = context.scene
        g_tools = scene.g_tools
        g_tools.mat_folder = editDir
        
        return {'FINISHED'}
    
    @staticmethod
    def yes(self, context):
        global editDirBool
        matDirList[self.index] = context.scene.g_tools.mat_folder
        editDirBool = False
        G_Modul.saveJsonFile(matDirList, "mat_folders", "resources")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_PT_CustomMaterial)
    bpy.utils.register_class(CustomMaterial)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_CustomMaterial)
    bpy.utils.unregister_class(CustomMaterial)
