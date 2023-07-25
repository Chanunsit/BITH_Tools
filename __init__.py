
bl_info = {
        "name": "BITH Setup Collisions",
        "description": "Setup suface and custom property and check collisions for Enfusion Engine",
        "author": "Gramma Team Thailand",
        "version": (1, 4),
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
from . import G_Panel_A




#
#Check patch version
addon_version = bl_info["version"]
addon_version_string = ".".join(map(str, addon_version))
#
classes = [G_Preferences, G_Object_info, G_Geometry_Prams, G_Main_Panel,
           G_Property, G_LODAnalyze, G_Utility,
           G_Panel_A,
           G_BatchExportPanel]

def register():
     for cls in classes:
          cls.register()
     
     G_Modul.addon_version = addon_version_string
     


def unregister():
     for cls in classes:
          cls.unregister()

     
    

if __name__ == '__main__':
     register()
