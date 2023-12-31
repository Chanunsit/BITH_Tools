import bpy

from bpy.types import Scene
from bpy.types import (PropertyGroup)
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)

from . import G_Modul, G_Icon_reg


class MyProperties(PropertyGroup):
    toolTab : EnumProperty(
        name="Tab",
        items = [("GEO", "Geometry", ""),
                 ("LOD", "LOD", ""),
                 ("UTIL", "Utility", ""),
                 ("INFO", "Info", "")
                 ]
        )
    
    safetyMode : BoolProperty(name="Safety Mode", default=False)
    report_surface = [""]
    report_property = [""]
    report_named = [""]
    
    ExportLocalList:StringProperty(name="Export Local List",default= "")
    text_Surface:StringProperty(name="text",default= "")
    text_Property:StringProperty(name="text",default= "")
    text_Named:StringProperty(name="text",default= "")
    check_collision:BoolProperty(name= "None",default= False)
    print_report: bpy.props.BoolProperty(default=False)
    favProperty : StringProperty(name="Favorite Property",default= "")
    favSurface : StringProperty(name="Favorite Surface",default= "")
    
    report_lod : StringProperty(name="Report LOD")
    report_tri : StringProperty(name="Report Triangle")

    shareMatList = G_Modul.loadJsonFile("share_mat", "resources")
    shareMat : EnumProperty(
    items=[(id, label, "") for i, (id, label) in enumerate(shareMatList)],
    description="Share Material")
    
    infoTab : EnumProperty(
        name="Tab",
        items = [("Arma", "Arma", "", G_Icon_reg.custom_icons["arma"].icon_id, 1),
                 ("DayZ", "DayZ", "", G_Icon_reg.custom_icons["dayz"].icon_id, 2),
                 ("Market", "Market", "", G_Icon_reg.custom_icons["market"].icon_id, 3)
                 ]
        )

    exportLocalList : StringProperty(name="Export Location List")
    
    custom_mat_panel : BoolProperty(name="Custom Material", default=False)
    mat_folder : StringProperty(name="Materials Path", subtype='DIR_PATH')
    cusMatList = G_Modul.loadJsonFile("custom_mat", "resources")
    if len(cusMatList) == 0:
        cusMatList = shareMatList
    cusMat : EnumProperty(name="Custom Material",
    items=[(id, label, "") for i, (id, label) in enumerate(cusMatList)],
    description="Custom Material")
    

classes = [MyProperties]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Scene.g_tools = PointerProperty(type= MyProperties)
   


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del Scene.g_tools
