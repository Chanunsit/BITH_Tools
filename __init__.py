
bl_info = {
        "name": "BITH Tools",
        "description": "Setup suface and custom property and check collisions for Enfusion Engine",
        "author": "Gramma Team Thailand",
        "version": (1, 5),
        "blender": (3, 4, 0),
        "location": "View3D",
        "warning": "", # used for warning icon and text in add-ons panel
        "wiki_url": "",
        "tracker_url": "",
        "support": "COMMUNITY",
        "category": "3D View",
        }

import bpy
import os
from . import G_Object_info
from . import G_Geometry_Prams
from . import G_Main_Panel
from . import G_Property
from . import G_BatchExportPanel
from . import G_LODAnalyze
from . import G_Preferences
from . import G_Utility
from . import G_Modul
from . import G_Web_info
from . import G_CustomMat



#
#Check patch version
addon_version = bl_info["version"]
addon_version_string = ".".join(map(str, addon_version))
#


def register():
     G_Preferences.register()
     G_Object_info.register()
     G_Geometry_Prams.register()
     G_Main_Panel.register()
     G_Property.register()
     G_LODAnalyze.register()
     G_CustomMat.register()
     G_BatchExportPanel.register()
     G_Utility.register()
     G_Web_info.register()
     
     
     G_Modul.addon_version = addon_version_string
     


def unregister():
     G_Preferences.unregister()
     G_Object_info.unregister()
     G_Geometry_Prams.unregister()
     G_Main_Panel.unregister()
     G_Property.unregister()
     G_LODAnalyze.unregister()
     G_BatchExportPanel.unregister()
     G_Utility.unregister()
     G_Web_info.unregister()
     G_CustomMat.unregister()
     
     
    

if __name__ == '__main__':
     register()
