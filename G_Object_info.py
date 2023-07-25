import bpy
import os
from bpy.types import Panel

class OBJECT_PT_ObjectInfoPanel(Panel):
    
    bl_label = "Object info"
    bl_idname = "OBJECT_PT_object_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '💠'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        #selected_objects = bpy.context.selected_objects
        # scene = context.scene
        # g_tools = scene.g_tools
        
    
        box = layout.box()
        line_height = 0.6
        row = box.row()
        row.label(text="", icon="OBJECT_DATA")
        row.prop(obj, "name", text="")
        box = layout.box()
        if obj:
            if obj.keys():
#                layout.label(text="Custom Properties:")
                for key in obj.keys():
                    row = box.row()
                    row.scale_y = line_height
                    name = obj.name
                    if "UBX_" in name or "UCX_" in name or "USP_" in name or "UCS_" in name or "UCL_" in name or "UTM_" in name :
                        if key != "usage":
                            row.alert = True
                            row.label(text="" + key + " : " + str(obj[key]),icon="PREFERENCES")
                            row.alert = False
                        else:
                            row.label(text="" + key + " : " + str(obj[key]),icon="PREFERENCES")
                    else:
                        if key != "usage":
                            row.label(text="" + key + " : " + str(obj[key]),icon="PREFERENCES")
                        else:
                            row.alert = True
                            row.label(text="" + key + " : " + str(obj[key]),icon="PREFERENCES")
                            row.alert = False
                            
                    row.operator("object.del_custom_prop_operator", text="", icon="TRASH").name = key
                    row = layout.row(align=True)

            else:
                row = box.row()
                row.scale_y = line_height
                row.label(text="", icon="PREFERENCES")
                row.label(text="")  
        box = layout.box()             
        row = layout.row()
        if obj.type == 'MESH':
            if obj.data.materials:
                
                for index, material in enumerate(obj.data.materials):
#                    material in obj.data.materials:
                    row = layout.row(align=True)
                    
                    # Input word
                    word = material.name

                    # Split the word using the separator "/"
                    word_parts = word.split("_")

                    # Create an empty list
                    word_list = []

                    # Append each part of the word to the list
                    for part in word_parts:
                        word_list.append(part)
                        #print(len(word_parts))

                    # Print the resulting list
                    #print(word_list.pop())
                    if len(word_list) >= 2 and len(word_list[-1]) == 16:
                        word_list.pop()
                        mat_name = " ".join(word_list)
                        mat_name = mat_name.capitalize()
                    else:
                        mat_name = word
                    #print(len(word_parts))
                    
                    row = box.row()
                    row.scale_y = line_height
                    name = obj.name
                    if "UBX_" in name or "UCX_" in name or "USP_" in name or "UCS_" in name or "UCL_" in name or "UTM_" in name :
                        if len(word_parts) >= 2 and len(word_parts[-1]) == 16:
                            row.label(text=""+str(index+1) +" : "+ mat_name,icon="MATERIAL")
                        else:
                            row.alert = True
                            row.label(text=""+str(index+1) +" : "+ mat_name,icon="MATERIAL")
                            row.alert = False
                    else:
                        if len(word_parts) >= 2 and len(word_parts[-1]) == 16:
                            row.alert = True
                            row.label(text=""+str(index+1) +" : "+ mat_name,icon="MATERIAL")
                            row.alert = False
                            
                        else:
                            row.label(text=""+str(index+1) +" : "+ mat_name,icon="MATERIAL")
                    row.operator("object.remove_mat", text="", icon="TRASH").matIndex = index
                    
                
            else:
                row = box.row()
                row.scale_y = line_height
                row.label(text="", icon="MATERIAL")
                row.label(text=" ")
        else:
            row = box.row()
            row.scale_y = line_height
            row.label(text="", icon="MATERIAL")

class OBJECT_OT_DelCustomProp(bpy.types.Operator):
    bl_idname = "object.del_custom_prop_operator"
    bl_label = "Delete All Custom Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_icon = "CON_TRANSFORM"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Delete all custom properties"

    name : bpy.props.StringProperty(name="Name")

    def execute(self, context):
        obj = bpy.context.object
        del obj[self.name]
        bpy.ops.object.checkobjcts(action="check")
        return {'FINISHED'}
        
class OBJECT_OT_RemoveMat(bpy.types.Operator):
    bl_idname = "object.remove_mat"
    bl_label = "Remove Material"
    
    matIndex : bpy.props.IntProperty(name="Index")
    def execute(self, context):
        #bpy.context.view_layer.objects.active = obj
        obj = bpy.context.object
        if obj.hide_get():
            hide = True
        else:
            hide = False
        obj.hide_set(False)
        if bpy.context.mode == 'EDIT_MESH':
            editMode = True
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            editMode = False
        obj = bpy.context.active_object
        obj.active_material_index = self.matIndex
        bpy.ops.object.material_slot_remove()
        if editMode:
            bpy.ops.object.mode_set(mode='EDIT')
        obj = bpy.context.object
        if hide:
            obj.hide_set(True)
        else:
            obj.hide_set(False)
        bpy.ops.object.checkobjcts(action="check")
        return {'FINISHED'}



def register():
    bpy.utils.register_class(OBJECT_OT_RemoveMat)
    bpy.utils.register_class(OBJECT_PT_ObjectInfoPanel)
    bpy.utils.register_class(OBJECT_OT_DelCustomProp)

    



def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RemoveMat)
    bpy.utils.unregister_class(OBJECT_PT_ObjectInfoPanel)
    bpy.utils.unregister_class(OBJECT_OT_DelCustomProp)
    
    



if __name__ == "__main__":
    register()
