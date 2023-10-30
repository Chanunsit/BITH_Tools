import bpy
import textwrap
from . import G_Modul
from . import G_Icon_reg
from . import G_Web_info

class VIEW3D_PT_MainPanel(bpy.types.Panel):
    bl_label = "BITH Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        g_tools = scene.g_tools
        layout.prop(g_tools, "toolTab", expand=True)
        row = layout.row()

        #-----------------------------------------Geometry---------------------------------------------
        
        if g_tools.toolTab == "GEO":
            row = layout.row()
            row.label(text="Setup Geometry")
            box = layout.box()
            row = box.row()
            row.prop(scene, "layer_preset",text="", icon="PREFERENCES",expand=False)
            #row = layout.row()        
            row.operator("object.assign_property", text="", icon="MOD_LINEART").action = "assign"
            row.operator("object.assign_property", text="", icon="SOLO_ON").action = "fav"
            
            if g_tools.favProperty:
                favList = G_Modul.string_to_list(g_tools.favProperty)
            else:
                favList = []
            if favList:
                #box = layout.box()
                for s in favList:
                    row = box.row()
                    row.label(text=s)
                    bt = row.operator("object.assign_property", text="", icon="MOD_LINEART")
                    bt.action = "assignFav"
                    bt.type = s
                    bt = row.operator("object.assign_property", text="", icon="TRASH")
                    bt.action = "favRemove"
                    bt.type = s
            
    
            # Add the assign material button
            box = layout.box()
            row = box.row()
            row.prop(scene, "Surface_Properties",text="", icon="MATERIAL")
            #row = layout.row()
            row.operator("object.assign_material", text="", icon="VIEWZOOM").action = "find"
            row.operator("object.assign_material", text="", icon="MOD_LINEART").action = "assign"
            row.operator("object.assign_material", text="", icon="SOLO_ON").action = "fav"
            
            if g_tools.favSurface:
                favList = G_Modul.string_to_list(g_tools.favSurface)
            else:
                favList = []
            if favList:
                #box = layout.box()
                for s in favList:
                    row = box.row()
                    row.label(text=s)
                    bt = row.operator("object.assign_material", text="", icon="MOD_LINEART")
                    bt.action = "assignFav"
                    bt.type = s
                    bt = row.operator("object.assign_material", text="", icon="TRASH")
                    bt.action = "favRemove"
                    bt.type = s
            box = layout.box()
            row = box.row()
            row.prop(g_tools, "shareMat", text="", icon="MATERIAL")
            row.operator("object.assign_share_material", text="", icon="MOD_LINEART").index = g_tools.shareMat
            # Add the assign layer preset button            
            layout.separator()
            row = layout.row()      
            
            row.operator("object.checkobjcts", text="Scan Error", icon="VIEWZOOM").action = "check" 
            #row.alignment = 'LEFT' 
            #row.alignment = 'RIGHT'
            print_report = context.scene.g_tools.print_report
            if g_tools.check_collision:
                prop_list = G_Modul.string_to_list(g_tools.text_Property)
                sur_list = G_Modul.string_to_list(g_tools.text_Surface)
                name_list = G_Modul.string_to_list(g_tools.text_Named)
                if len(prop_list) == 0 and len(sur_list) == 0 and len(name_list) == 0:
                    print_report = False

            if  print_report:
                row.operator("object.checkobjcts", text="", icon="TRIA_DOWN").action = "expan"
            else:
                row.operator("object.checkobjcts", text="", icon="TRIA_LEFT").action = "expan"
            row = layout.row() 
            
            if  print_report:
                if g_tools.check_collision:
                    my_list = G_Modul.string_to_list(g_tools.text_Property)
                    if len(my_list) != 0:
                        box = layout.box()
                        row.label(text="Property", icon="ERROR")
                        row = layout.row()
                    
                        for item in my_list:
                            row = box.row()
                            obj = context.object
                            
                            try:
                                if obj.name == item:
                                    row.label(text="▶  "+str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_OFF")
                                else:
                                    row.label(text=str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            except:
                                row.label(text=str(item))
                                button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            button.action = "select"
                            button.objName = item
                            obj = bpy.data.objects.get(item)
                            if obj.hide_get():
                                button = row.operator("object.checkobjcts", text="", icon="HIDE_ON")
                            else:
                                button = row.operator("object.checkobjcts", text="", icon="HIDE_OFF")
                            button.action = "hide"
                            button.objName = item 
                            
                    row = layout.row() 
                    my_list = G_Modul.string_to_list(g_tools.text_Surface)
                    if len(my_list) != 0:
                        box = layout.box()
                        row.label(text="Surface", icon="ERROR")
                        row = layout.row()
                    
                        for item in my_list:
                            row = box.row()
                            obj = context.object
                            
                            try:
                                if obj.name == item:
                                    row.label(text="▶  "+str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_OFF")
                                else:
                                    row.label(text=str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            except:
                                row.label(text=str(item))
                                button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            button.action = "select"
                            button.objName = item
                            obj = bpy.data.objects.get(item)
                            if obj.hide_get():
                                button = row.operator("object.checkobjcts", text="", icon="HIDE_ON")
                            else:
                                button = row.operator("object.checkobjcts", text="", icon="HIDE_OFF")
                            button.action = "hide"
                            button.objName = item
                            
                    row = layout.row()   
                    my_list = G_Modul.string_to_list(g_tools.text_Named)
                    if len(my_list) != 0:
                        box = layout.box()
                        row.label(text="Name", icon="ERROR")
                        row = layout.row()
                    
                        for item in my_list:
                            row = box.row()
                            obj = context.object
                            try:
                                if obj.name == item:
                                    row.label(text="▶  "+str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_OFF")
                                else:
                                    row.label(text=str(item))
                                    button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            except:
                                row.label(text=str(item))
                                button = row.operator("object.checkobjcts", text="", icon="RESTRICT_SELECT_ON")
                            button.action = "select"
                            button.objName = item
                            obj = bpy.data.objects.get(item)
                            try:
                                if obj.hide_get():
                                    button = row.operator("object.checkobjcts", text="", icon="HIDE_ON")
                                else:
                                    button = row.operator("object.checkobjcts", text="", icon="HIDE_OFF")
                            except:
                                button = row.operator("object.checkobjcts", text="", icon="HIDE_OFF")
                            button.action = "hide"
                            button.objName = item
           

        #-----------------------------------------LOD---------------------------------------------
        elif g_tools.toolTab == "LOD":
            row = layout.row()
            row.label(text="LOD Tools")
            row = layout.row()
            row.operator("object.lod_analyze").action = "analyze"
        
            if g_tools.report_lod and g_tools.report_lod != "[]" and g_tools.report_tri and g_tools.report_tri != "[]":
                box = layout.box()
                lod_list = G_Modul.string_to_list(g_tools.report_lod)
                tri_list = G_Modul.string_to_list(g_tools.report_tri)
                for i in range(len(lod_list)):
                    row = box.row()
                    if i == 0:
                        row.label(text="LOD"+ lod_list[i][0][-1] + " : " + str(tri_list[i]))
                    else:
                        if tri_list[i] > tri_list[i-1]*0.5:
                            row.alert = True
                            row.label(text="LOD"+ lod_list[i][0][-1] + " : " + str(tri_list[i]))
                            row.alert = False
                        else:
                            row.label(text="LOD"+ lod_list[i][0][-1] + " : " + str(tri_list[i]))
                    bt = row.operator("object.lod_analyze", text="", icon="RESTRICT_SELECT_OFF")
                    bt.action = "isolate"
                    bt.index = i

        #-----------------------------------------Utility---------------------------------------------
        elif g_tools.toolTab == "UTIL":
            row = layout.row()
            row.label(text="Utility Tools")
            box = layout.box()
            box.label(text="Custom Material")
            row = box.row()
            row.prop(g_tools, "cusMat", text="", icon="MATERIAL")
            row.operator("object.custom_materials", text="", icon="MOD_LINEART").action = "set"
            row = box.row()
            row.prop(g_tools, "custom_mat_panel", text="Setting")
            #row = layout.row()
            
       #-----------------------------------------Web information---------------------------------------------
        elif g_tools.toolTab == "INFO":
            row = layout.row()
            #row = layout.row(align=True)
            #row.alignment = 'LEFT'
            row.label(text="Information : ")
            row = layout.row()
            row.prop(g_tools, "infoTab", expand=True)
            row = layout.row()
            if g_tools.infoTab == "Arma":
                layout.prop(context.scene, "selected_website_arma4", text="")
                box = layout.box()
                selected_website = bpy.context.scene.selected_website_arma4
                selected_description = next(desc for url, name, desc in G_Web_info.website_arma4 if url == selected_website)
                G_Modul.TextWrap(context, selected_description, box, 0.5)
                row = layout.row()
                row.operator("addon.open_selected_website_arma4", text="Open Website")
            elif g_tools.infoTab == "DayZ":
                layout.prop(context.scene, "selected_website_dayz", text="")
                box = layout.box()
                selected_website = bpy.context.scene.selected_website_dayz
                selected_description = next(desc for url, name, desc in G_Web_info.website_dayZ if url == selected_website)
                G_Modul.TextWrap(context, selected_description, box, 0.5)
                row = layout.row()
                row.operator("addon.open_selected_website_dayz", text="Open Website")
            elif g_tools.infoTab == "Market":
                layout.prop(context.scene, "selected_website_market", text="")
                box = layout.box()
                selected_website = bpy.context.scene.selected_website_market
                selected_description = next(desc for url, name, desc in G_Web_info.website_market if url == selected_website)
                G_Modul.TextWrap(context, selected_description, box, 0.5)
                row = layout.row()
                row.operator("addon.open_selected_website_market", text="Open Website")
            


def register():
    bpy.utils.register_class(VIEW3D_PT_MainPanel)

    
   
    
    
    

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MainPanel)
