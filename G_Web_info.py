import bpy

# Define a list of website options with descriptions
website_arma4 = [
    ("https://confluence.bistudio.com/display/ARMA4/Art+Guidelines#tab-STRUCTURES",
    "Art Guidelines",
    "All infomation and rule Art for armma4. $/nYou should know this!"),

    ("https://confluence.bistudio.com/display/~mario/Arma4+modeling+and+texturing+rules+for+houses",
    "Rules for houses",
    "modeling and texturing rules for houses."),

    ("https://confluence.bistudio.com/display/ARMA4/Metrics",
    "Rule Metrics",
    "rule dimention for asset in arma4 you must follow this."),
    
    ("https://confluence.bistudio.com/display/ARMA4/Structure+Art+Workflow+-+WIP",
    "Structure Art Workflow",
    "Expand structure Art Workflow "),

     ("https://confluence.bistudio.com/display/~pinamat/Small+props+and+structures+destruction+guideline",
    "Destruction guideline",
    "Show example destruction for structure and small prop"),
    
    ("https://confluence.bistudio.com/display/ARMA4/Vegetation+Pipeline#18458022532d5ae4e962f4c148655f035cd0e4916",
    "Vegetation guideline",
    "Expand step how to make vegetation for arma4"),
    
    ("https://confluence.bistudio.com/pages/viewpage.action?spaceKey=ARMA4&postingDay=2022%2F11%2F7&title=Arma+Reforger+and+Arma+4+SVN+split",
    "Arma 4 SVN",
    "Link to access Arma 4 SVN"),
    
    ("https://confluence.bistudio.com/pages/viewpage.action?pageId=242868430",
    "Light portals & model internal BSP trees",
    "They are a solution for faking global $/nillumination effects by adding virtual lights $/ninto building portals, i.e., windows, doors, openings"),
]

# Properties for storing the selected website and its description
bpy.types.Scene.selected_website_arma4 = bpy.props.EnumProperty(
    name="Select Website",
    items=[(url, name, desc) for url, name, desc in website_arma4]
)

class OpenSelectedWebsiteArma(bpy.types.Operator):
    bl_idname = "addon.open_selected_website_arma4"
    bl_label = "Open Selected Website"

    def execute(self, context):
        selected_website_url = context.scene.selected_website_arma4

        # Open the selected website in a web browser
        bpy.ops.wm.url_open(url=selected_website_url)

        return {'FINISHED'}
#========================================================================================================================#

website_dayZ = [
    ("https://confluence.bistudio.com/display/ARMA4/Art+Guidelines#tab-STRUCTURES",
    "DayZ",
    "Day ZDay ZDay ZDay ZDay $/n$/sZDay ZDay ZDay ZDay ZDay ZDay ZDay ZDay $/n$/hZDayZDayZDayZDayZ"),
]

# Properties for storing the selected website and its description
bpy.types.Scene.selected_website_dayz = bpy.props.EnumProperty(
    name="Select Website",
    items=[(url, name, desc) for url, name, desc in website_dayZ]
)

class OpenSelectedWebsiteDayZ(bpy.types.Operator):
    bl_idname = "addon.open_selected_website_dayz"
    bl_label = "Open Selected Website"

    def execute(self, context):
        selected_website_url = context.scene.selected_website_dayz

        # Open the selected website in a web browser
        bpy.ops.wm.url_open(url=selected_website_url)

        return {'FINISHED'}

#========================================================================================================================#

website_market = [
    ("https://bohemiainteractive.sharepoint.com/sites/art/Sources/Forms/AllItems.aspx?newTargetListUrl=%2Fsites%2Fart%2FSources&viewpath=%2Fsites%2Fart%2FSources%2FForms%2FAllItems%2Easpx&id=%2Fsites%2Fart%2FSources%2FAddons&viewid=5f229a07%2Da329%2D46e7%2Da3a5%2D33d44e47ab74",
    "From BI",
    "Addon in this link has purchased from Bohemie Interactive"),

    ("https://drive.google.com/drive/folders/1r73DZ7QPJecxSL8oz-RDXR2ZMXIrFFqr?usp=sharing",
    "DuckX Tools",
    "Utility Addon $/n$/sshotcut D $/n$/hCreated by Kanong Manuree[wAy]")
]

# Properties for storing the selected website and its description
bpy.types.Scene.selected_website_market = bpy.props.EnumProperty(
    name="Select Website",
    items=[(url, name, desc) for url, name, desc in website_market]
)

class OpenSelectedWebsiteMarket(bpy.types.Operator):
    bl_idname = "addon.open_selected_website_market"
    bl_label = "Open Selected Website"

    def execute(self, context):
        selected_website_url = context.scene.selected_website_market

        # Open the selected website in a web browser
        bpy.ops.wm.url_open(url=selected_website_url)

        return {'FINISHED'}

#========================================================================================================================#


def register():
    bpy.utils.register_class(OpenSelectedWebsiteArma)
    bpy.utils.register_class(OpenSelectedWebsiteDayZ)
    bpy.utils.register_class(OpenSelectedWebsiteMarket)

def unregister():
    bpy.utils.unregister_class(OpenSelectedWebsiteArma)
    bpy.utils.unregister_class(OpenSelectedWebsiteDayZ)
    bpy.utils.unregister_class(OpenSelectedWebsiteMarket)