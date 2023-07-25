import bpy
import os
from bpy.types import Panel

class VIEW3D_PT_PanelA(Panel):
    
    bl_label = "Panel A"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'

    @classmethod
    def poll(cls, context):
        scene = context.scene
        g_tools = scene.g_tools
        return g_tools.toolTab == "UTIL"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test Panel on Utilitab")





def register():
    bpy.utils.register_class(VIEW3D_PT_PanelA)

    



def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_PanelA)

    