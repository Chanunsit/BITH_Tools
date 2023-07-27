import bpy
import os
from . import G_Modul

class AssignShareMat(bpy.types.Operator):
    bl_idname = "object.assign_share_material"
    bl_label = "Assign Share Material"

    index : bpy.props.StringProperty(name="Index")

    def execute(self, context):
        index = self.index
        activeObject = bpy.context.active_object
        activeObject.data.materials.clear()
        mat = G_Modul.create_material(index)
        activeObject.data.materials.append(mat)
        mat.use_nodes = True
        index = index.split("/")
        index = index.pop()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project()
        bpy.context.area.ui_type = 'UV'
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.align_rotation(method='GEOMETRY', axis='Z')
        bpy.ops.uv.align_rotation(method='AUTO')
        bpy.context.area.ui_type = 'VIEW_3D'
        
        if bpy.context.space_data.shading.type == 'SOLID':
            bpy.context.space_data.shading.color_type = 'TEXTURE'
        texture_name = index.capitalize()
        texture_path = os.path.join(os.path.dirname(__file__), "TexSurface")
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
      
        tree = mat.node_tree
        
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

        return {'FINISHED'}
    


def register():
    bpy.utils.register_class(AssignShareMat)

    
   
    
    
    

def unregister():
    bpy.utils.unregister_class(AssignShareMat)
