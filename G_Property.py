import bpy

from bpy.types import Scene
from bpy.types import (PropertyGroup)
from bpy.props import (EnumProperty, PointerProperty, StringProperty, FloatVectorProperty, FloatProperty, IntProperty, BoolProperty)

from . import G_Modul


class MyProperties(PropertyGroup):
    toolTab : EnumProperty(
        name="Tab",
        items = [("GEO", "Geometry", ""),
                 ("LOD", "LOD", ""),
                 ("UTIL", "Utility", "")
                 ]
        )
    
    safetyMode : BoolProperty(name="Safety Mode", default=True)
    
    report_surface = [""]
    report_property = [""]
    report_named = [""]
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
    description="Share Material"
    )

classes = [MyProperties]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Scene.g_tools = PointerProperty(type= MyProperties)
   


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del Scene.g_tools
