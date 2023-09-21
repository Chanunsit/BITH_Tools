import bpy
import json
import os
import shutil
import distutils
import urllib.request
import zipfile
import json
import textwrap
import re
#import requests

from . import G_Geometry_Prams

def create_material(material_name):
    # Check if the material already exists in the scene
    if material_name in bpy.data.materials:
        return bpy.data.materials[material_name]

    # If the material does not exist, create a new material
    material = bpy.data.materials.new(name=material_name)

    # Assign the material to the active object's active material slot
    active_object = bpy.context.active_object
    if active_object and active_object.type == 'MESH':
        material_slot = active_object.material_slots.get(material_name)
        if material_slot:
            material_slot.material = material

    return material

def check_material_slot(object, material_name):
    for slot in object.material_slots:
        if slot.material and slot.material.name == material_name:
            return True
    return False


def get_all_children(col):
    yield col
    for child in col.children:
        yield from get_all_children(child)

def get_object_name():
# Get the current scene
    object_names = []
    # scene = bpy.context.scene
    # object_names = [obj.name for obj in scene.objects]
    view_layer = bpy.context.view_layer
    for layer_col in get_all_children(view_layer.layer_collection):
        if not layer_col.exclude:
            for obj in layer_col.collection.objects:
                object_names.append(obj.name)
    return object_names # ส่งค่าออกไป

#____________เช็ก material__________________
def check_surface(name):
    report_surface = ""
    obj = bpy.data.objects.get(name)
    
    if "UBX_" in name or "UCX_" in name or "USP_" in name or "UCS_" in name or "UCL_" in name or "UTM_" in name : 
        # Get the material slots from the object
        material_slots = obj.material_slots   
        # Create a list to store the material slot names
        material_slot_names = []
        if obj.data.materials:
            for slot in material_slots:
                material_slot_names.append(slot.name)
                # print(material_slot_names)
        if obj.data.materials:
            for i in range(len(material_slot_names)):
                matname = material_slot_names[i].split("_")
                matname = matname.pop()
                # if not "Common/Materials/" in material_slot_names[i]:       
                #     report_surface = name 
                if not material_check(material_slot_names[i]):
                    report_surface = name
        else:  report_surface = name  
            
    return report_surface

#____________Check collision__________________
def check_property(name):
    report_property = ""
    if "UBX_" in name or "UCX_" in name or "USP_" in name or "UCS_" in name or "UCL_" in name or "UTM_" in name :
        obj = bpy.data.objects.get(name)
        if not obj.get("usage"): 
            # print(name + " No Property")
            report_property = name
    return report_property
#        else:
#            print("Right")

def check_named(name):
    report_named = ""
    obj = bpy.data.objects.get(name)
    if obj.get("usage"):
        if not "UBX_" in name and not "UCX_" in name and not "USP_" in name and not "UCS_" in name and not "UCL_" in name and not "UTM_" in name : 
            report_named = name
    if obj.type == 'MESH':
        material_slots = obj.material_slots   
        material_slot_names = []
        if obj.data.materials:
            for slot in material_slots:
                material_slot_names.append(slot.name)
        if obj.data.materials:
            for i in range(len(material_slot_names)):
                matname = material_slot_names[i].split("_")
                matname = matname.pop()
                if material_check(material_slot_names[i]):
                    if not "UBX_" in name and not "UCX_" in name and not "USP_" in name and not "UCS_" in name and not "UCL_" in name and not "UTM_" in name :
                        report_named = name
    return report_named

def material_check(matName):
    check = False
    surFaceList = list_to_string(G_Geometry_Prams.Surface_Properties)
    if matName in surFaceList:
        check = True
    else:
        check = False
    return check
    

def find_lod(name):
    lodList = []
    report_lod = []
    for _name in name:
        n = _name.split("_")
        n = n.pop()
        n = n.upper()
        if len(n) == 4: 
            if n[0] == "L" and n[1] == "O" and n[2] == "D":
                lodList.append(_name)
    lodList = sorted(lodList, key=lambda item: int(item.split('_')[-1][3:]))
    for item in lodList:
        lod_number = item.split('_')[-1] 
        for group in report_lod:
            if lod_number in group[0]:
                group.append(item)
                break
        else:
            report_lod.append([item])
    return report_lod

def select_objects_by_name(name_list):
    for obj in bpy.context.scene.objects:
        if obj.name in name_list:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
        else:
            obj.select_set(False)

def triangle_call():
    selected_objects = bpy.context.selected_objects
    num_triangles = 0
    if selected_objects is not None:
        for obj in selected_objects:
            if obj.type == 'MESH':
                mesh = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
                num_triangles += sum(len(p.vertices) - 2 for p in mesh.polygons)
            else:
                return 0 
        return(num_triangles)

def focus_object_in_outliner():
    for area in [a for a in bpy.context.screen.areas if a.type == 'OUTLINER']:
        for region in [r for r in area.regions if r.type == 'WINDOW']:
            override = {'area':area, 'region': region}
            bpy.ops.outliner.show_active(override)

def list_to_string(list):
    # Convert list to a JSON-formatted string
    try:
        string = json.dumps(list)
    except:
        print("")
    return string

def string_to_list(string):
    # Convert the JSON-formatted string back to a list
    try:
        list = json.loads(string)
    except:
        print("")
    return list

def saveJsonFile(list, fileName, location):
    addon_path = os.path.dirname(__file__)
    directory = os.path.join(addon_path, location)

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, fileName + ".json")

    with open(file_path, 'w') as f:
        json.dump(list, f)
        
def loadJsonFile(fileName, location):
    addon_directory = os.path.dirname(__file__)
    resources_directory = os.path.join(addon_directory, location)
    json_file_path = os.path.join(resources_directory, fileName + ".json")

    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            data = json.load(file)
            file.close()
    else:
        print("JSON file not found.")
    return data


addon_version=""
def get_addon_version():
    # this is set in __init__
    return addon_version

dlProg = ""
extProg = ""
def update_addon(self, context, zip_filename):
    try:
        os.remove(zip_filename)
    except:
        print("No file update")
    try:
        UPDATED_ADDON_URL = url = "https://github.com/Chanunsit/BITH_Tools/archive/refs/heads/" + zip_filename
        # Get the addon directory and the current addon file path
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        addon_file = os.path.join(addon_dir, "__init__.py")
        # Download the updated addon zip file
        def download_progress(block_count, block_size, total_size):
            downloaded = block_count * block_size
            percent = int((downloaded / total_size) * 100)
            global dlProg
            
            percent = 100
            dlProg = f"Downloaded: {percent}%"
            print(f"Downloaded: {percent}%")

        urllib.request.urlretrieve(UPDATED_ADDON_URL, filename=zip_filename, reporthook=download_progress)

        scene = context.scene
        g_tools = scene.g_tools
        if not g_tools.safetyMode:
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                total_files = len(zip_ref.infolist())
                extracted_files = 0
                for file_info in zip_ref.infolist():
                    zip_ref.extract(file_info, addon_dir)
                    extracted_files += 1
                    percent = int((extracted_files / total_files) * 100)
                    global extProg
                    if percent > 100:
                        percent = 100
                    extProg = f"Extracted: {percent}%"
                    print(f"Extracted: {percent}%")
        else:
            percent = 100
            extProg = f"Extracted: {percent}%"
        # Remove the downloaded zip file
        os.remove(zip_filename)
        src  = os.path.join(os.path.dirname(__file__), "BITH_Tools-main")
        copy_and_move_files(src)
        # folder_path = os.getcwd()
        # print(folder_path+"\\BITH_Tools-main")
        try:
            #os.rmdir("BITH_Tools-main")
            src  = os.path.join(os.path.dirname(__file__), "BITH_Tools-main")
            shutil.rmtree(src)
            print("Delete BITH_Tools-main folder")
        except:
            print("Error delete BITH_Tools-main folder")
        #shutil.rmtree("BITH_Tools-main")
        # Reload the addon module
        #bpy.ops.script.reload()
        self.report({'INFO'}, "Addon Updated. Please Restart Blender.")
    except:
        self.report({'INFO'}, "Addon Updater Error")

    
def update_patch(filename):
    try:
        UPDATED_ADDON_URL = url = "https://github.com/Chanunsit/BITH_Tools/releases/download/BITH_Tools/" + filename
        # Get the patch directory
        patch_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "patch")
        # Ensure the "patch" folder exists; if not, create it
        os.makedirs(patch_dir, exist_ok=True)
        # Download the updated addon file
        response = urllib.request.urlopen(UPDATED_ADDON_URL)
        data = response.read()
        # Save the updated addon file in the patch directory
        updated_addon_file = os.path.join(patch_dir, filename)
        with open(updated_addon_file, "wb") as f:
            f.write(data)

        print("Check Addon Updated.")
    except:
        print("Check Addon Updated Error")
 

 
        
def read_txt_file(filename, location):
    patch_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), location)
    file_path = os.path.join(patch_dir, filename)
    try:
        with open(file_path, "r") as file:
            lines = file.read().splitlines()
            return lines
    except FileNotFoundError:
        print(f"File '{filename}' not found in the 'patch' folder.")
        return None
    except Exception as e:
        print(f"Error occurred while reading the file: {e}")
        return None


def refresh_panel():
    for area in bpy.context.workspace.screens[0].areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'UI':
                            region.tag_redraw()
                            break
                        
def copy_and_move_files(src):
    try:
        dst  = os.path.dirname(os.path.realpath(__file__))
        files = os.listdir(src)

        print(src)
        print(files)
        print(dst)

        distutils.dir_util.copy_tree(src, dst)

        print("Files copied and moved successfully.")
    except Exception as e:
        print("An error occurred:", str(e))
        
        
def TextWrap(context, text, parent, line_height):
    texts = text.split("$/n")
    for text in texts:
        chars = int(context.region.width / 7)   # 7 pix on 1 character
        wrapper = textwrap.TextWrapper(width=chars)
        text_lines = wrapper.wrap(text=text)
        if "$/h" in text_lines[0]:
            text_lines[0] = text_lines[0].replace("$/h","")
            for i in range(len(text_lines)):
                text_lines[i] = "$/h" + text_lines[i]
        if "$/s" in text_lines[0]:
            text_lines[0] = text_lines[0].replace("$/s","")
            for i in range(len(text_lines)):
                text_lines[i] = "$/s" + text_lines[i]
        for text_line in text_lines:
            row = parent.row(align=True)
            if "$/h" in text_line:
                row.alert = True
                text_line = text_line.replace("$/h","")
            if "$/s" in text_line:
                row.enabled = False
                text_line = text_line.replace("$/s","") 
            row.label(text=text_line)
            row.scale_y = line_height
            
            
def get_meta(meta_text):
    pattern = r'Name "{(.*?)}(.*?)"'
    match = re.search(pattern, meta_text)
    if match:
        id = match.group(1)
        name = match.group(2)
        return id, name
    else:
        return None, None
    

def find_meta_files(folder_path):
    meta_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".meta"):
                meta_files.append(os.path.join(root, file))

    return meta_files


def read_meta_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the contents of the .meta file
            meta_contents = file.read()
        return meta_contents
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
