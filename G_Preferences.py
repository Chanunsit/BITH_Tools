import bpy


import time

from bpy.types import Menu, Operator, Panel, AddonPreferences, PropertyGroup
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)

from . import G_Modul
from . import G_Geometry_Prams


confirm = False
checkUpdate = False
updated = False
patch = []
selectVer = ""
urlID = ""
patchNote = []
text = ""

class PT_Preferences(AddonPreferences):
     bl_idname = __package__
     
     def draw(self, context):
          scene = context.scene
          g_tools = scene.g_tools
          layout = self.layout
          box = layout.box()
          box.label(text="Materials Path")
          box.prop(g_tools, "mat_folder", text="")
          box.operator(GetMaterials.bl_idname)
          row = layout.row()
          row = layout.row()
          row.operator(Updater.bl_idname, text="Check Patch").action = "check"
          if checkUpdate:
               box = layout.box()
               row = box.row()
               if confirm:
                    row.operator(Updater.bl_idname, text="Yes").action = "yes"
                    row.operator(Updater.bl_idname, text="No").action = "no"
               # else:
               #      for ver in patch:
               #           bt = row.operator(Updater.bl_idname, text=ver[0])
               #           bt.action = "update"
               #           bt.index = ver[0]
               
               if patchNote is not None and updated == False:
                    for line in patchNote:
                         row = box.row()
                         row.scale_y = 0.5
                         row.label(text=line)
               if updated:
                    #row = box.row()
                    row.scale_y = 0.5
                    row.label(text=text)
          row = layout.row()
          row.prop(g_tools, "safetyMode")

        

class Updater(Operator):
     bl_idname = "object.updater_operator"
     bl_label = "Update Addon"
     
     action : StringProperty(name="Action")
     index : StringProperty(name="Index")
     url_id : StringProperty(name="ID") 

     def execute(self, context):
          scene = context.scene
          G_Modul.dlProg = ""
          G_Modul.extProg = ""
          if self.action == "check":
              self.check(self, context)
          elif self.action == "update":
               self.update(self, context)
          elif self.action == "yes":
               self.yes(self, context)
          elif self.action == "no":
              self.no(self, context)
          return {'FINISHED'}
     @staticmethod
     def check(self, context):
          global updated, patchNote, checkUpdate, confirm
          updated = False
          confirm = True
          print("Addon version : " + G_Modul.get_addon_version())
          fileName = 'a_patch.json'
          G_Modul.update_patch(fileName)
          global patch
          patch = G_Modul.loadJsonFile("a_patch", "patch")
          print("All patch : " + G_Modul.list_to_string(patch))
          lastPatch = patch[-1]
          print("Last patch : " + lastPatch[0])
          if float(G_Modul.addon_version) < float(lastPatch[0]):
               print("Update Now")
          else:
               print("Latest")
          G_Modul.update_patch("patch_note.txt")
          patchNote = G_Modul.read_txt_file("patch_note.txt", "patch")
          checkUpdate = True
          return {'FINISHED'}
     @staticmethod
     def update(self, context):
          global selectVer, updated, urlID, confirm
          selectVer = self.index
          urlID = self.url_id
          confirm = True
          updated = False
          return {'FINISHED'}
     @staticmethod
     def yes(self, context):
          #bpy.ops.wm.console_toggle()
          #fileName = "bith_tools_" + selectVer  + ".zip"
          fileName = "main.zip"
          G_Modul.update_addon(self, context,fileName)
          global text, confirm, updated
          text = "Addon  " + G_Modul.dlProg + "  and  "  + G_Modul.extProg + "  Please Restart Blender  "
          confirm = False
          updated = True
          print(selectVer)
          print(urlID)
          return {'FINISHED'}
     @staticmethod
     def no(self, context):
          global confirm, updated
          confirm = False
          updated = False
          return {'FINISHED'}


class GetMaterials(Operator):
     bl_idname = "object.get_materials"
     bl_label = "Get Materials"
     def execute(self, context):
          scene = context.scene
          g_tools = scene.g_tools
          matName = []
          matFiles = G_Modul.find_meta_files(g_tools.mat_folder)
          if matFiles is not None:
               for path in matFiles:
                    matFile = G_Modul.read_meta_file(path)
                    id, name = G_Modul.get_meta(matFile)
                    mat = []
                    name = name.split("/")
                    name = name[-1].split(".")
                    name = name[0]
                    #print(name + "_" + id)
                    mat.append(name + "_" + id)
                    mat.append(name)
                    matName.append(mat)
                    #print(matName)
          #print(G_Geometry_Prams.Surface_Properties)
          G_Geometry_Prams.Surface_Properties = matName
          #G_Geometry_Prams.Surface_Properties.append(matName)
          print(G_Geometry_Prams.Surface_Properties)
          G_Geometry_Prams.enumSurface_Properties()
          return {'FINISHED'}


classes = [PT_Preferences, Updater, GetMaterials]


def register():
     for cls in classes:
        bpy.utils.register_class(cls)
        

def unregister():
     for cls in classes:
        bpy.utils.unregister_class(cls)
        
