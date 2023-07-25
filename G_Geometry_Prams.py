import bpy
import os
import bmesh
from . import G_Modul
from . import G_Icon_reg

Surface_Properties = G_Modul.loadJsonFile("Surface_Properties", "resources")
# Define the Texture path
# texture_path = "C:\Create_Image\output_directory"
texture_path = os.path.join(os.path.dirname(__file__), "TexSurface")

def check_material_name(material_name):
    obj = bpy.context.active_object
    if obj.type != 'MESH':
        return False

    for slot in obj.material_slots:
        if slot.material and slot.material.name == material_name:
            return True

    return False

def select_material_slots(material_name):
    obj = bpy.context.active_object
    if obj.type != 'MESH':
        return

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for i, slot in enumerate(obj.material_slots):
        if slot.material and slot.material.name == material_name:
            obj.active_material_index = i
            #obj.material_slots[i].select = True

    bpy.ops.object.mode_set(mode='EDIT')
# Define a function for the material selection callback
def material_selection_callback(self, context):
    self.assign_material_button_enabled = True

# Define a function to find the texture file using the label
def assign_material_button_callback(self, context):
    material_name = context.scene.Surface_Properties
    material_label = context.scene.Surface_Properties
    material_name = None
    # Get the active object
    obj = context.active_object
    for name, label in Surface_Properties:
        if label == material_label:
            material_name = name
            break
              
    if material_name is None:
        return  # Material with the specified label not found
    
    # Check if the material exists
    material = bpy.data.materials.get(material_name)
    
    # Create a new material if it doesn't exist
    if material is None:
        material = bpy.data.materials.new(name=material_name)
        print("Created new material:", material.name)
        
    if material_name == "category":
        return  # Return without assigning any material
# ________________________________________________________________  
    if bpy.context.object.mode == 'OBJECT': 
        # Assign the material to the selected object
        selected_obj = bpy.context.object
        
        # Clear all existing material slots
        selected_obj.data.materials.clear()
        
        # Create a new material slot and assign the material
        selected_obj.data.materials.append(material)
        print("Assigned material:", material.name, "to object:", selected_obj.name)
        # Auto UV        
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.context.area.ui_type = 'UV'
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.align_rotation(method='GEOMETRY', axis='Z')
        bpy.ops.transform.resize(value=(5, 5, 5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.area.ui_type = 'VIEW_3D'
        bpy.ops.object.editmode_toggle()
    else:
        print("It's not Object")
        
    if bpy.context.object.mode == 'EDIT':
        # Get the mesh data
        mesh = obj.data

        # Create a BMesh object from the mesh data
        bm = bmesh.from_edit_mesh(mesh)

        # Get the selected faces
        selected_faces = [f for f in bm.faces if f.select]
        
        # Check if any faces are selected
        if selected_faces:
            # Auto UV
            bpy.ops.uv.smart_project()
            bpy.context.area.ui_type = 'UV'
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.align_rotation(method='GEOMETRY', axis='Z')
            
            bpy.context.area.ui_type = 'VIEW_3D'
        
            # Assign the material to the active object
            obj = bpy.context.active_object
            
            if check_material_name(material.name):
                select_material_slots(material.name)
            else:
                obj.data.materials.append(material)
                select_material_slots(material.name)

            bpy.ops.object.material_slot_assign()

            # Update the viewport
            bpy.context.view_layer.update()
        else:
            self.report({'INFO'}, "No faces selected.")
    else:
        self.report({'INFO'}, "Object is not in Edit Mode.")
# ________________________________________________________________   
    
    if bpy.context.space_data.shading.type == 'SOLID':
        bpy.context.space_data.shading.color_type = 'TEXTURE'

    # Set the texture for the material
    texture_name = material_label.capitalize()
    texture_file = os.path.join(texture_path, f"{texture_name}.jpg")
    
    if os.path.exists(texture_file):
        # Check if the texture with the desired name already exists
        existing_texture = bpy.data.textures.get(texture_name)
        
        if existing_texture is None:
            # If the texture doesn't exist, create a new one
            texture = bpy.data.textures.new(name=texture_name, type='IMAGE')
            texture.image = bpy.data.images.load(texture_file)
        else:
            # If the texture already exists, reuse it
            texture = existing_texture
      
        material.use_nodes = True
        tree = material.node_tree
        
        for node in tree.nodes:
            tree.nodes.remove(node)
        
        tex_coord = tree.nodes.new(type='ShaderNodeTexCoord')
        mapping = tree.nodes.new(type='ShaderNodeMapping')
        image_tex = tree.nodes.new(type='ShaderNodeTexImage')
        diffuse = tree.nodes.new(type='ShaderNodeBsdfDiffuse')
        output = tree.nodes.new(type='ShaderNodeOutputMaterial')
        
        tree.links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
        tree.links.new(mapping.outputs['Vector'], image_tex.inputs['Vector'])
        tree.links.new(image_tex.outputs['Color'], diffuse.inputs['Color'])
        tree.links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
        
        image_tex.image = texture.image
        print (texture_name)
        # bpy.data.images[texture_name].use_fake_user = True
          
    # add fake user to all images
    images = bpy.data.images
    for image in images:
        image.use_fake_user = True
    
    scene = context.scene
    try:
        scene.td.units = "1"
        scene.td.texture_size = "1"
        bpy.ops.object.preset_set(td_value="2048")

    except:
        print("Request Texel Density")
        self.report({"INFO"} ,"Request Texel Density")

def iconSurface(label):
    icon = "SHADING_RENDERED"
    if "metal_" in label.lower() or "Metal" in label or "iron_" in label.lower() or "linoleum" in label.lower() or "titanium" in label.lower():
        icon = "metal"
    elif "armor_" in label.lower() or "Armor" in label:
        icon = "armor"
    elif "fabric" in label.lower() or "carpet" in label.lower():
        icon = "fabric"
    elif "glass" in label.lower():
        icon = "glass"
    elif "grass_" in label.lower() or "Grass" in label or "seaweed" in label.lower():
        icon = "grass"
    elif "paper" in label.lower():
        icon = "paper"
    elif "plastic_" in label.lower() or "Plastic" in label:
        icon = "plastic"
    elif "rubber" in label.lower():
        icon = "rubber"
    elif "pebbles" in label.lower() or "cobblestone" in label.lower() or "gravel" in label.lower() or "Stone" in label:
        icon = "pebbles"
    elif "tiles" in label.lower():
        icon = "tiles"
    elif "vehicle" in label.lower():
        icon = "vehicle"
    elif "weapon_plastic" in label.lower() or "weapon_wood" in label.lower() or "weapon_metal" in label.lower():
        icon = "weapon"
    elif "wood" in label.lower():
        icon = "wood"
    elif "snow" in label.lower() or "water" in label.lower() or "moss" in label.lower() or "ice" in label.lower():
        icon = "environment"
    elif "brick" in label.lower():
        icon = "brick"
    elif "concrete" in label.lower():
        icon = "concrete"
    elif "asphalt" in label.lower():
        icon = "asphalt"
    elif "flesh" in label.lower():
        icon = "flesh"
    elif "foliage" in label.lower():
        icon = "foliage"
    elif "dirt" in label.lower() or "skids" in label.lower() or "sand" in label.lower() or "sand_beach" in label.lower() or "soil" in label.lower():
        icon = "dirt"
    elif "_______________" in label.lower():
        icon = "void"
    else:
        icon = "mat_default"
    return icon
# Create a material selection property
bpy.types.Scene.Surface_Properties = bpy.props.EnumProperty(
    items=[(label, label, "", G_Icon_reg.custom_icons[iconSurface(label)].icon_id, i) for i, (_, label) in enumerate(Surface_Properties)],
    description="Surface_Properties",
    update=material_selection_callback
)

# Create an assign material button property
bpy.types.Scene.assign_material_button_enabled = bpy.props.BoolProperty(default=False)

#--------------------------------------------------------------------------------------------------------------

layer_preset = G_Modul.loadJsonFile("layer_preset", "resources")

def Update_object(self, context):
    print("")
#    selected_object_names = [obj.name for obj in selected_objects]

def update_selected_option(self, context):
#    selected_objects = bpy.context.selected_objects
    object_name = context.object.name
    layer_preset = context.scene.layer_preset
    obj = bpy.context.active_object
    obj["usage"] = layer_preset
   
    if object_name in bpy.data.objects:
# Set the active object to the one with the specified name
        bpy.context.view_layer.objects.active = bpy.data.objects[object_name]
# Select the object
        bpy.data.objects[object_name].select_set(True)
# Update the scene to reflect the changes
        bpy.context.view_layer.update()
        print("Object", object_name, "selected.")
    else:
        print("Object", object_name, "does not exist in the scene.")

# Add a custom property to the object
bpy.types.Scene.layer_preset = bpy.props.EnumProperty(
    items=[(option, option, '') for option in layer_preset],
#    update=Update_object
)
#--------------------------------------------------------------------------------------------------------------
# panel
   

                       
                        
                

#--------------------------------------------------------------------------------------------------------------


    
class OBJECT_OT_AssignMaterialOperator(bpy.types.Operator):
    bl_idname = "object.assign_material"
    bl_label = "Assign Material"

    action : bpy.props.StringProperty(name="Action")
    type : bpy.props.StringProperty(name="Type")
    search : bpy.props.StringProperty(name="Search")

    def invoke(self, context, event):
        if self.action == "find":
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        g_tools = scene.g_tools
        row.prop(self, "search")
        search = self.search
        if g_tools.favSurface:
            favList = G_Modul.string_to_list(g_tools.favSurface)
        else:
            favList = []
        if search != "":
            
            for name in Surface_Properties:
                if search.lower() in name[1].lower():
                    row = layout.row()
                    row.label(text=name[1], icon_value=G_Icon_reg.custom_icons[iconSurface(name[1])].icon_id)
                    if favList:
                        if name[1] in favList:
                            bt = row.operator("object.assign_material", text="", icon="SOLO_ON")
                            bt.action = "favRemove"
                            bt.type = name[1]
                        else:
                            bt = row.operator("object.assign_material", text="", icon="SOLO_OFF")
                            bt.action = "favByName"
                            bt.type = name[1]
                    else:
                        bt = row.operator("object.assign_material", text="", icon="SOLO_OFF")
                        bt.action = "favByName"
                        bt.type = name[1]

    def execute(self, context):
        action = self.action
        if action == "assign":
            self.assign(self, context)
        elif action == "fav":
            self.fav(self, context)
        elif action == "favByName":
            self.favByName(self, context)
        elif action == "favRemove":
            self.favRemove(self, context)
        elif action == "assignFav":
            self.assignFav(self, context)
        # elif action == "find":
        #     self.find(self, context)
        return {'FINISHED'}
    @staticmethod
    def assign(self, context):
        obj = bpy.context.object
        if obj.hide_get():
            hide = True
        else:
            hide = False
        obj.hide_set(False)
        if bpy.context.scene.tool_settings.use_uv_select_sync == True:
            uvSync = True
        else:
            uvSync = False
        bpy.context.scene.tool_settings.use_uv_select_sync = False
        assign_material_button_callback(self, context)
        bpy.ops.object.checkobjcts(action="check")
        if uvSync == True:
            bpy.context.scene.tool_settings.use_uv_select_sync = True
        else:
            bpy.context.scene.tool_settings.use_uv_select_sync = False
        obj = bpy.context.object
        if hide:
            obj.hide_set(True)
        else:
            obj.hide_set(False)
        return {'FINISHED'}
    
    @staticmethod
    def fav(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        if not g_tools.favSurface:
            favList = []
        else:
            favList = G_Modul.string_to_list(g_tools.favSurface)
        favList.append(scene.Surface_Properties)
        g_tools.favSurface = G_Modul.list_to_string(favList)
        return {'FINISHED'}
    @staticmethod
    def favByName(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        if not g_tools.favSurface:
            favList = []
        else:
            favList = G_Modul.string_to_list(g_tools.favSurface)
        favList.append(self.type)
        g_tools.favSurface = G_Modul.list_to_string(favList)
        return {'FINISHED'}
    
    @staticmethod
    def favRemove(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        favList = G_Modul.string_to_list(g_tools.favSurface)
        favList.remove(self.type)
        g_tools.favSurface = G_Modul.list_to_string(favList)
        print(g_tools.favSurface)
        return {'FINISHED'}
    
    @staticmethod
    def assignFav(self, context):
        scene = context.scene
        scene.Surface_Properties = self.type
        bpy.ops.object.assign_material(action="assign")
        return {'FINISHED'}
    
    @staticmethod
    def find(self, context):
        print("FIND")
        return {'FINISHED'}
    
    def searcher():
        print("Searching...........")
        return {'FINISHED'}
    




class Add_Property(bpy.types.Operator):
    bl_idname = "object.assign_property"
    bl_label = "Set Property"

    action : bpy.props.StringProperty(name="Action")
    type : bpy.props.StringProperty(name="Type")
    
    def execute(self, context):
        action = self.action
        if action == "assign":
            self.assign(self, context)
        elif action == "fav":
            self.fav(self, context)
        elif action == "favRemove":
            self.favRemove(self, context)
        elif action == "assignFav":
            self.assignFav(self, context)
        return {'FINISHED'}
    
    @staticmethod
    def assign(self, context):
        obj = bpy.context.object
        if obj.hide_get():
            hide = True
        else:
            hide = False
        obj.hide_set(False)
        update_selected_option(self, context)
        bpy.ops.object.checkobjcts(action="check")
        obj = bpy.context.object
        if hide:
            obj.hide_set(True)
        else:
            obj.hide_set(False)
        return {'FINISHED'}
    
    @staticmethod
    def fav(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        if not g_tools.favProperty:
            favList = []
        else:
            favList = G_Modul.string_to_list(g_tools.favProperty)
        favList.append(scene.layer_preset)
        g_tools.favProperty = G_Modul.list_to_string(favList)
        return {'FINISHED'}
    
    @staticmethod
    def favRemove(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        favList = G_Modul.string_to_list(g_tools.favProperty)
        favList.remove(self.type)
        g_tools.favProperty = G_Modul.list_to_string(favList)
        print(g_tools.favProperty)
        return {'FINISHED'}
    
    @staticmethod
    def assignFav(self, context):
        scene = context.scene
        scene.layer_preset = self.type
        bpy.ops.object.assign_property(action="assign")
        return {'FINISHED'}


class OBJECT_OT_Checkobjects(bpy.types.Operator):
    bl_idname = "object.checkobjcts"
    bl_label = "Check Collision"

    action : bpy.props.StringProperty(name="Action")
    objName : bpy.props.StringProperty(name="Object Name")
    
    def execute(self, context):
        if self.action == "expan":
            self.expan(self, context)
        elif self.action == "check":
            self.check(self, context)
        elif self.action == "select":
            self.selectObject(self, context)
        elif self.action == "hide":
            self.hide(self, context)
        else:       
            pass
        
  
        return {'FINISHED'}
    
    @staticmethod
    def check(self, context):
        
        scene = context.scene
        g_tools = scene.g_tools
        g_tools.report_surface =[]
        g_tools.report_property =[]
        g_tools.report_named =[]
        for name in G_Modul.get_object_name():
            # G_modul.check_property(name)
            # G_modul.check_surface(name)
            # G_modul.check_named(name)

            g_tools.report_surface.append( G_Modul.check_surface(name))   
            g_tools.report_property.append( G_Modul.check_property(name))  
            g_tools.report_named.append(G_Modul.check_named(name))

        while("" in g_tools.report_surface):
            g_tools.report_surface.remove("")
        while("" in g_tools.report_property):
            g_tools.report_property.remove("")
        while("" in g_tools.report_named):
            g_tools.report_named.remove("") 
            
        g_tools.text_Surface= G_Modul.list_to_string(g_tools.report_surface)
        g_tools.text_Property= G_Modul.list_to_string(g_tools.report_property)
        g_tools.text_Named= G_Modul.list_to_string(g_tools.report_named)
        
        scene = context.scene
        g_tools = scene.g_tools
        g_tools.print_report = True
        g_tools.check_collision = True
    
    @staticmethod
    def expan(self, context):
        scene = context.scene
        g_tools = scene.g_tools
        if g_tools.print_report:
            g_tools.print_report = False
        else:
            g_tools.print_report = True
        #context.scene.print_report = not context.scene.print_report
        return {'FINISHED'}
    
    @staticmethod
    def selectObject(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[self.objName]
        bpy.data.objects[self.objName].select_set(True)
        G_Modul.focus_object_in_outliner()
        return {'FINISHED'}
    
    @staticmethod
    def hide(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[self.objName]
        bpy.data.objects[self.objName].select_set(True)
        obj = bpy.context.object
        if obj.hide_get():
            obj.hide_set(False)
        else:
            obj.hide_set(True)
   
        return {'FINISHED'}
    
    


# Register the material selection panel, property, and operator
def register():
    bpy.utils.register_class(OBJECT_OT_AssignMaterialOperator)
    bpy.utils.register_class(Add_Property)
    bpy.utils.register_class(OBJECT_OT_Checkobjects)

    
   
    
    
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_AssignMaterialOperator)
    bpy.utils.unregister_class(Add_Property)
    bpy.utils.unregister_class(OBJECT_OT_Checkobjects)
    
