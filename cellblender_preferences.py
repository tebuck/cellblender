# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

"""
This file contains the classes for CellBlender's Preferences.

"""

import cellblender

# blender imports
import bpy
from bpy.app.handlers import persistent
from bl_operators.presets import AddPresetBase
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
                      FloatProperty, FloatVectorProperty, IntProperty, \
                      IntVectorProperty, BoolVectorProperty, PointerProperty, StringProperty

#from bpy.app.handlers import persistent
#import math
#import mathutils

# python imports
import re

# CellBlender imports
import cellblender
from . import parameter_system
# from . import cellblender_operators
from . import cellblender_utils


# We use per module class registration/unregistration
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


def check_mcell_binary(self, context):
    """Callback to check for mcell executable"""
    mcell = context.scene.mcell
    binary_path = mcell.cellblender_preferences.mcell_binary
    mcell.cellblender_preferences.mcell_binary_valid = cellblender_utils.is_executable(binary_path)
    bpy.ops.mcell.preferences_save(name='Cb')
    return None

def check_python_binary(self, context):
    """Callback to check for python executable"""
    mcell = context.scene.mcell
    binary_path = mcell.cellblender_preferences.python_binary
    mcell.cellblender_preferences.python_binary_valid = cellblender_utils.is_executable(binary_path)
    bpy.ops.mcell.preferences_save(name='Cb')
    return None

def check_bionetgen_location(self, context):
    """Callback to check for mcell executable"""
    mcell = context.scene.mcell
    application_path = mcell.cellblender_preferences.bionetgen_location
    mcell.cellblender_preferences.bionetgen_location_valid = cellblender_utils.is_executable(application_path)
    bpy.ops.mcell.preferences_save(name='Cb')
    return None



from . import cellblender_panels

def set_old_scene_panels_callback(self, context):
    """ Show or hide the old scene panels based on the show_old_scene_panels boolean property. """
    print ( "Toggling the old scene panels" )
    mcell = context.scene.mcell
    prefs = mcell.cellblender_preferences
    if (prefs.show_scene_panel or prefs.show_tool_panel):
        # One of the other panels is showing, so it's OK to toggle
        show_old_scene_panels ( prefs.show_old_scene_panels )
    else:
        # No other panels are showing so DON'T ALLOW THIS ONE TO GO AWAY!
        prefs.show_old_scene_panels = True
        show_old_scene_panels ( True )


def set_scene_panel_callback(self, context):
    """ Show or hide the scene panel based on the show_scene_panel boolean property. """
    print ( "Toggling the scene panel" )
    mcell = context.scene.mcell
    prefs = mcell.cellblender_preferences
    if (prefs.show_old_scene_panels or prefs.show_tool_panel):
        # One of the other panels is showing, so it's OK to toggle
        show_hide_scene_panel ( prefs.show_scene_panel )
    else:
        # No other panels are showing so DON'T ALLOW THIS ONE TO GO AWAY!
        prefs.show_scene_panel = True
        show_hide_scene_panel ( True )


def set_tool_panel_callback(self, context):
    """ Show or hide the tool panel based on the show_tool_panel boolean property. """
    print ( "Toggling the tool panels" )
    mcell = context.scene.mcell
    prefs = mcell.cellblender_preferences
    if (prefs.show_old_scene_panels or prefs.show_scene_panel):
        # One of the other panels is showing, so it's OK to toggle
        show_hide_tool_panel ( prefs.show_tool_panel )
    else:
        # No other panels are showing so DON'T ALLOW THIS ONE TO GO AWAY!
        prefs.show_tool_panel = True
        show_hide_tool_panel ( True )


# Callback Functions must be defined before being used:

def set_tab_autocomplete_callback ( self, context ):
    # print ( "Called with self.tab_autocomplete = " + str(self.tab_autocomplete) )
    if self.tab_autocomplete:
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.indent'].active = False
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.autocomplete'].type = 'TAB'
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.autocomplete'].ctrl = False
    else:
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.autocomplete'].type = 'SPACE'
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.autocomplete'].ctrl = True
        bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Console'].keymap_items['console.indent'].active = True


def set_double_sided_callback ( self, context ):
    for mesh in bpy.data.meshes:
        mesh.show_double_sided = self.double_sided

def set_backface_culling_callback ( self, context ):
    # bpy.data.window_managers[0].windows[0].screen.areas[4].spaces[0].show_backface_culling = True        
    for wm in bpy.data.window_managers:
        for w in wm.windows:
            for a in w.screen.areas:
                for s in a.spaces:
                    if s.type == 'VIEW_3D':
                        s.show_backface_culling = self.backface_culling




# Operators can't be callbacks, so we need this function.
def save_preferences(self, context):
    bpy.ops.mcell.preferences_save(name='Cb')
    return None



@persistent
def load_preferences(context):
    """ Load CB preferences using preset on startup. """
    print ( "load post handler: cellblender_operators.load_preferences() called" )

    #active_preset = bpy.types.MCELL_MT_presets.bl_label
    #bpy.ops.script.execute_preset(
    #    filepath=preset_path, menu_idname="MCELL_MT_presets")

    # Cant use execute_preset here because of incorrect context
    # Look for existing preset named "Cb" in "cellblender" preset subdir
    # Presets are named with leading capital, but modules are lowercase
    # Therefore the preset "Cb" corresponds to the file "cb.py"
    try:
        preset_path = bpy.utils.preset_find(
            "Cb", 'cellblender', display_name=True)
        with open(preset_path, 'r') as preset_file:
            preset_string = preset_file.read()
            exec(preset_string)
    except TypeError:
        print('No preset file found')


class MCELL_OT_save_preferences(AddPresetBase, bpy.types.Operator):
    """Save CellBlender Preferences."""

    bl_idname = "mcell.preferences_save"
    bl_label = "Save Preferences"
    # This needs to be the same name as the preset menu class in
    # cellblender_panels
    preset_menu = "MCELL_MT_presets" 

    preset_defines = [
        "scene = bpy.context.scene"
    ]

    # These are the values which will be saved/loaded
    preset_values = [
        "scene.mcell.cellblender_preferences.mcell_binary",
        "scene.mcell.cellblender_preferences.bionetgen_location",
        "scene.mcell.cellblender_preferences.python_binary",
        "scene.mcell.cellblender_preferences.decouple_export_run",
        "scene.mcell.cellblender_preferences.invalid_policy",
    ]

    # This needs to be the same as what's in the menu class
    preset_subdir = "cellblender" 


class MCELL_OT_reset_preferences(bpy.types.Operator):
    """Reset CellBlender preferences"""

    bl_idname = "mcell.preferences_reset"
    bl_label = "Reset Preferences"
    bl_description = ("Reset preferences to their original values.")
    bl_options = {'REGISTER'}

    def execute(self, context):
        mcell = context.scene.mcell
        mcell.cellblender_preferences.mcell_binary = ""
        mcell.cellblender_preferences.python_binary = ""
        mcell.cellblender_preferences.bionetgen_location = ""
        mcell.cellblender_preferences.invalid_policy = 'dont_run'
        mcell.cellblender_preferences.decouple_export_run = False

        return {'FINISHED'}





class MCELL_OT_set_mcell_binary(bpy.types.Operator):
    bl_idname = "mcell.set_mcell_binary"
    bl_label = "Set MCell Binary"
    bl_description = ("Set MCell Binary. If needed, download at "
                      "mcell.org/download.html")
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        mcell = context.scene.mcell
        mcell.cellblender_preferences.mcell_binary = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class MCELL_OT_set_python_binary(bpy.types.Operator):
    bl_idname = "mcell.set_python_binary"
    bl_label = "Set Python Binary"
    bl_description = "Set Python Binary"
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        mcell = context.scene.mcell
        mcell.cellblender_preferences.python_binary = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class MCELL_OT_set_check_bionetgen_location(bpy.types.Operator):
    bl_idname = "mcell.set_bionetgen_location"
    bl_label = "Set BioNetGen Location"
    bl_description = ("Set BioNetGen Location. If needed, download at "
                      "bionetgen.org")
    bl_options = {'REGISTER'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH', default="")

    def execute(self, context):
        mcell = context.scene.mcell
        mcell.cellblender_preferences.bionetgen_location = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




class CellBlenderPreferencesPropertyGroup(bpy.types.PropertyGroup):

    mcell_binary = StringProperty(name="MCell Binary",
        update=check_mcell_binary)
    mcell_binary_valid = BoolProperty(name="MCell Binary Valid",
        default=False)
    python_binary = StringProperty(name="Python Binary",
        update=check_python_binary)
    python_binary_valid = BoolProperty(name="Python Binary Valid",
        default=False)
    bionetgen_location = StringProperty(name="BioNetGen Location",
        update=check_bionetgen_location)
    bionetgen_location_valid = BoolProperty(name="BioNetGen Location Valid",
        default=False)

    invalid_policy_enum = [
        ('dont_run', "Do not run with errors", ""),
        ('filter', "Filter errors and run", ""),
        ('ignore', "Ignore errors and attempt run", "")]
    invalid_policy = EnumProperty(
        items=invalid_policy_enum,
        name="Invalid Policy",
        default='dont_run',
        update=save_preferences)
    decouple_export_run = BoolProperty(
        name="Decouple Export and Run", default=False,
        description="Allow the project to be exported without also running"
                    " the simulation.",
        update=save_preferences)
    debug_level = IntProperty(
        name="Debug", default=0, min=0, max=100,
        description="Amount of debug information to print: 0 to 100")
    
    use_long_menus = BoolProperty(
        name="Show Long Menu Buttons", default=True,
        description="Show Menu Buttons with Text Labels")

    use_stock_icons = BoolProperty (
        name="Use only internal Blender Icons", default=True,
        description="Use only internal Blender Icons")


    show_extra_options = BoolProperty (
        name="Show Extra Options", default=False,
        description="Show Additional Options (mostly for debugging)" )

    show_button_num = BoolVectorProperty ( size=15, default=[True for i in range(15)] )


    show_old_scene_panels = BoolProperty(
        name="Old CellBlender in Scene Tab", default=True,
        description="Show Old CellBlender Panels in Scene Tab", update=set_old_scene_panels_callback)

    show_scene_panel = BoolProperty(
        name="CellBlender in Scene Tab", default=True,
        description="Show CellBlender Panel in Scene Tab", update=set_scene_panel_callback)

    show_tool_panel = BoolProperty(
        name="CellBlender in Tool Tab", default=True,
        description="Show CellBlender Panel in Tool Tab", update=set_tool_panel_callback)

    show_sim_runner_options = BoolProperty(name="Show Alternate Simulation Runners", default=False)

    tab_autocomplete = BoolProperty(name="Use tab for console autocomplete", default=False, update=set_tab_autocomplete_callback)
    double_sided = BoolProperty(name="Show Double Sided Mesh Objects", default=False, update=set_double_sided_callback)
    backface_culling = BoolProperty(name="Backface Culling", default=False, update=set_backface_culling_callback)



    def remove_properties ( self, context ):
        print ( "Removing all Preferences Properties... no collections to remove." )


    def draw_layout(self, context, layout):
        mcell = context.scene.mcell

        if not mcell.initialized:
            mcell.draw_uninitialized ( layout )
        else:
            row = layout.row(align=True)
            row.operator("mcell.preferences_reset")
            layout.separator()

            row = layout.row()
            row.operator("mcell.set_mcell_binary",
                         text="Set Path to MCell Binary", icon='FILESEL')
            row = layout.row()
            mcell_binary = self.mcell_binary
            if not mcell_binary:
                row.label("MCell Binary not set", icon='UNPINNED')
            elif not self.mcell_binary_valid:
                row.label("MCell File/Permissions Error: " +
                    self.mcell_binary, icon='ERROR')
            else:
                row.label(
                    text="MCell Binary: "+self.mcell_binary,
                    icon='FILE_TICK')

            row = layout.row()
            row.operator("mcell.set_bionetgen_location",
                         text="Set Path to BioNetGen File", icon='FILESEL')
            row = layout.row()
            bionetgen_location = self.bionetgen_location
            if not bionetgen_location:
                row.label("BioNetGen location not set", icon='UNPINNED')
            elif not self.bionetgen_location_valid:
                row.label("BioNetGen File/Permissions Error: " +
                    self.bionetgen_location, icon='ERROR')
            else:
                row.label(
                    text="BioNetGen Location: " + self.bionetgen_location,
                    icon='FILE_TICK')

            row = layout.row()
            row.operator("mcell.set_python_binary",
                         text="Set Path to Python Binary", icon='FILESEL')
            row = layout.row()
            python_path = self.python_binary
            if not python_path:
                row.label("Python Binary not set", icon='UNPINNED')
            elif not self.python_binary_valid:
                row.label("Python File/Permissions Error: " +
                    self.python_binary, icon='ERROR')
            else:
                row.label(
                    text="Python Binary: " + self.python_binary,
                    icon='FILE_TICK')

            row = layout.row()
            row.prop(mcell.cellblender_preferences, "decouple_export_run")
            row = layout.row()
            row.prop(mcell.cellblender_preferences, "invalid_policy")

            layout.separator()

            row = layout.row()
            row.prop ( context.user_preferences.inputs, "view_rotate_method" )
            
            row = layout.row()
            row.prop(mcell.cellblender_preferences, "use_long_menus")

            row = layout.row()
            row.prop(mcell.cellblender_preferences, "use_stock_icons")

            row = layout.row()
            row.prop ( context.user_preferences.system, "use_vertex_buffer_objects", text="Enable Vertex Buffer Objects" )
            
            row = layout.row()
            row.prop ( mcell.cellblender_preferences, "backface_culling", text="Enable Backface Culling" )

            row = layout.row()
            row.prop ( mcell.cellblender_preferences, "double_sided" )

            box = layout.box()

            row = box.row(align=True)
            row.alignment = 'LEFT'
            if self.show_extra_options:
                row.prop(self, "show_extra_options", icon='TRIA_DOWN', emboss=False)

                row = box.row()
                row.prop(mcell.cellblender_preferences, "tab_autocomplete")
                row = box.row()
                row.prop(mcell.cellblender_preferences, "show_tool_panel")
                row = box.row()
                row.prop(mcell.cellblender_preferences, "show_scene_panel")
                row = box.row()
                row.prop(mcell.cellblender_preferences, "show_old_scene_panels")

                row = box.row()
                row.prop(mcell.cellblender_preferences, "show_sim_runner_options")


                row = box.row()
                row.label ( "Enable/Disable individual short menu buttons:" )
                row = box.row()
                row.prop(mcell.cellblender_preferences, "show_button_num", text="")


            else:
                row.prop(self, "show_extra_options", icon='TRIA_RIGHT', emboss=False)
                

            


            #row.operator ( "mcell.reregister_panels", text="Show CB Panels",icon='ZOOMIN')
            #row.operator ( "mcell.unregister_panels", text="Hide CB Panels",icon='ZOOMOUT')
            

    def draw_panel ( self, context, panel ):
        """ Create a layout from the panel and draw into it """
        layout = panel.layout
        self.draw_layout ( context, layout )



#CellBlendereGUI Panels:
class MCELL_PT_cellblender_preferences(bpy.types.Panel):
    bl_label = "CellBlender - Preferences"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw ( self, context ):
        # Call the draw function of the object itself
        context.scene.mcell.cellblender_preferences.draw_panel ( context, self )

