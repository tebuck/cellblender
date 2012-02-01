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


bl_info = {
    "name": "CellBlender",
    "author": "Tom Bartol",
    "version": (0,1),
    "blender": (2, 6, 1),
    "api": 42614,
    "location": "Properties > Scene > CellBlender Panel",
    "description": "CellBlender Modeling System for MCell",
    "warning": "",
    "wiki_url": "http://www.mcell.cnl.salk.edu",
    "tracker_url": "",
    "category": "Cell Modeling"
}


import bpy
from bpy.app.handlers import persistent
import mathutils
import os
import glob
import resource
import re
import random
from math import *



# See notes below for errors in documentation


# CellBlender GUI Panels:

class MCELL_PT_project_settings(bpy.types.Panel):
  bl_label = "CellBlender Project Settings"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()
    row.operator("mcell.set_project_dir",text="Set CellBlender Project Directory",icon="FILESEL")
    row = layout.row()
    row.label(text="Project Directory:  "+mc.project_settings.project_dir)
    row = layout.row()
    layout.prop(mc.project_settings,"base_name")
    layout.separator()
    row = layout.row()
    row.label(text="Export Project")
    row = layout.row()
    layout.prop(mc.project_settings,"export_format")
    row = layout.row()
    layout.prop(mc.project_settings,"export_selection_only")
    row = layout.row()
    row.operator("mcell.export_project",text="Export CellBlender Project",icon="FILESEL")



class MCELL_PT_sim_control(bpy.types.Panel):
  bl_label = "Simulation Control"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_viz_results(bpy.types.Panel):
  bl_label = "Visualize Simulation Results"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    
    mc = context.scene.mcell
    
    row=layout.row()
    row.operator("mcell.set_mol_viz_dir",text="Set Molecule Viz Directory",icon="FILESEL")
    #    layout.prop(mc,"mol_file_path",text="Molecule Viz Directory")
    row = layout.row()
    row.label(text="Molecule Viz Directory:  "+mc.mol_viz.mol_file_dir)
    row = layout.row()
    row.label(text="Current Molecule File:  "+mc.mol_viz.mol_file_name)
    row = layout.row()
    row.template_list(mc.mol_viz,"mol_file_list",mc.mol_viz,"mol_file_index",rows=2)
    row = layout.row()
    layout.prop(mc.mol_viz,"render_and_save")

#    col = row.column(align=True)
#    col.operator("mcell.mol_viz_prev",icon="PLAY_REVERSE",text="")
#    col = row.column(align=True)
#    col.operator("mcell.mol_viz_set_index",text=str(mc.mol_viz.mol_file_index))
#    col = row.column(align=True)
#    col.operator("mcell.mol_viz_next",icon="PLAY",text="")
    



class MCELL_PT_utilities(bpy.types.Panel):
  bl_label = "Utilities"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_user_model_parameters(bpy.types.Panel):
  bl_label = "User-Defined Model Parameters"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_initialization(bpy.types.Panel):
  bl_label = "MCell Model Initialization"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_define_molecules(bpy.types.Panel):
  bl_label = "Define Molecules"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    
    mc = context.scene.mcell
    
    row = layout.row()
    row.label(text="Defined Molecules:", icon='FORCE_LENNARDJONES')
    row = layout.row()
    col = row.column()
    col.template_list(mc,"species_list",mc,"active_mol_index",rows=2)
    col = row.column(align=True)
    col.operator("mcell.molecule_add",icon='ZOOMIN',text="")
    col.operator("mcell.molecule_remove",icon='ZOOMOUT',text="")
    if len(mc.species_list)>0:
      mol = mc.species_list[mc.active_mol_index]
      layout.prop(mol,"name")
      layout.prop(mol,"type")
      layout.prop(mol,"diffusion_constant")
      layout.prop(mol,"target_only")
      layout.prop(mol,"custom_time_step")
      layout.prop(mol,"custom_space_step")



class MCELL_PT_define_reactions(bpy.types.Panel):
  bl_label = "Define Reactions"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row = layout.row()
    row.label(text="Defined Reactions:", icon='FORCE_LENNARDJONES')
    row = layout.row()
    col = row.column()
    col.template_list(mc.reactions,"reaction_list",mc.reactions,"active_rxn_index",rows=2)
    col = row.column(align=True)
    col.operator("mcell.reaction_add",icon='ZOOMIN',text="")
    col.operator("mcell.reaction_remove",icon='ZOOMOUT',text="")
    if len(mc.reactions.reaction_list)>0:
      rxn = mc.reactions.reaction_list[mc.reactions.active_rxn_index]
      layout.prop(rxn,"reactants")
      layout.prop(rxn,"type")
      layout.prop(rxn,"products")
      layout.prop(rxn,"fwd_rate")
      if rxn.type == "reversible":
        layout.prop(rxn,"bkwd_rate")
      layout.prop(rxn,"rxn_name")



class MCELL_PT_define_surface_classes(bpy.types.Panel):
  bl_label = "Define Surface Classes"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_molecule_placement(bpy.types.Panel):
  bl_label = "Molecule Placement"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_reaction_output_settings(bpy.types.Panel):
  bl_label = "Reaction Output Settings"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_visualization_output_settings(bpy.types.Panel):
  bl_label = "Visualization Output Settings"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "scene"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    mc = context.scene.mcell
    
    row=layout.row()



class MCELL_PT_define_surface_regions(bpy.types.Panel):
  bl_label = "Define Surface Regions"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "object"
  bl_options = {'DEFAULT_CLOSED'}
  
  def draw(self, context):
    layout = self.layout
    
    obj_regs = context.object.mcell.regions
    aobj = context.active_object
    
    row = layout.row()
    row.label(text="Defined Regions:", icon='FORCE_LENNARDJONES')
    row = layout.row()
    col = row.column()
    col.template_list(obj_regs,"region_list",obj_regs,"active_reg_index",rows=2)
    col = row.column(align=True)
    col.operator("mcell.region_add",icon='ZOOMIN',text="")
    col.operator("mcell.region_remove",icon='ZOOMOUT',text="")
    row = layout.row()
    if len(obj_regs.region_list)>0:
      reg = obj_regs.region_list[obj_regs.active_reg_index]
      layout.prop(reg,"name")
    if aobj.mode == 'EDIT':
      row = layout.row(align=True)
      row.operator("mcell.region_faces_assign",text="assign")
      row.operator("mcell.region_faces_remove",text="remove")
      row.operator("mcell.region_faces_select",text="select")
      row.operator("mcell.region_faces_deselect",text="deselect")


#Custom Properties

class MCellSurfaceRegionFaceProperty(bpy.types.PropertyGroup):
  index = bpy.props.IntProperty(name="Face Index")


class MCellSurfaceRegionProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Region Name")
  faces = bpy.props.CollectionProperty(type=MCellSurfaceRegionFaceProperty,name="Surface Region List")
  active_face_index = bpy.props.IntProperty(name="Active Face Index",default=0)


class MCellSurfaceRegionListProperty(bpy.types.PropertyGroup):
  region_list = bpy.props.CollectionProperty(type=MCellSurfaceRegionProperty,name="Surface Region List")
  active_reg_index = bpy.props.IntProperty(name="Active Region Index",default=0)


class MCellSpeciesProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Molecule Name")
  type_enum = [
                    ('2D','Surface Molecule',''),
                    ('3D','Volume Molecule','')]
  type = bpy.props.EnumProperty(items=type_enum,name="Molecule Type")
  diffusion_constant = bpy.props.FloatProperty(name="Diffusion Constant",precision=4)
  target_only = bpy.props.BoolProperty(name="Target Only")
  custom_time_step = bpy.props.FloatProperty(name="Custom Time Step")
  custom_space_step = bpy.props.FloatProperty(name="Custom Space Step")
  

# Generic PropertyGroup to hold strings for a ColletionProperty  
class MCellStringProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Text")


class MCellReactionProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="The Reaction")
  rxn_name = bpy.props.StringProperty(name="Reaction Name")
  reactants = bpy.props.StringProperty(name="Reactants")
  products = bpy.props.StringProperty(name="Products")
  type_enum = [
                ('irreversible','->',''),
                ('reversible','<->','')]
  type = bpy.props.EnumProperty(items=type_enum,name="Reaction Type")
  fwd_rate = bpy.props.FloatProperty(name="Forward Rate",precision=4)
  bkwd_rate = bpy.props.FloatProperty(name="Backward Rate",precision=4)


#Panel Properties:

class MCellProjectPanelProperty(bpy.types.PropertyGroup):
  base_name = bpy.props.StringProperty(name="Project Base Name")
  project_dir = bpy.props.StringProperty(name="Project Directory")
  export_format_enum = [
                         ('mcell_mdl','MCell MDL Format','')]
  export_format = bpy.props.EnumProperty(items=export_format_enum,name="Export Format",default="mcell_mdl")
  export_selection_only = bpy.props.BoolProperty(name="Export Selected Objects Only",default=True)


# Property group for for molecule visualization (Visualize Simulation Results Panel)
class MCellMolVizPanelProperty(bpy.types.PropertyGroup):
  mol_file_dir = bpy.props.StringProperty(name="Molecule File Dir",subtype="NONE")
  mol_file_list = bpy.props.CollectionProperty(type=MCellStringProperty,name="Molecule File Name List")
  mol_file_num = bpy.props.IntProperty(name="Number of Molecule Files",default=0)
  mol_file_name = bpy.props.StringProperty(name="Current Molecule File Name",subtype="NONE")
  mol_file_index = bpy.props.IntProperty(name="Current Molecule File Index",default=0)
  mol_file_start_index = bpy.props.IntProperty(name="Molecule File Start Index",default=0)
  mol_file_stop_index = bpy.props.IntProperty(name="Molecule File Stop Index",default=0)
  mol_file_step_index = bpy.props.IntProperty(name="Molecule File Step Index",default=1)
  mol_viz_list = bpy.props.CollectionProperty(type=MCellStringProperty,name="Molecule Viz Name List")
  render_and_save = bpy.props.BoolProperty(name="Render & Save Images")


class MCellReactionsPanelProperty(bpy.types.PropertyGroup):
  reaction_list = bpy.props.CollectionProperty(type=MCellReactionProperty,name="Reaction List")
  active_rxn_index = bpy.props.IntProperty(name="Active Reaction Index",default=0)



# Main MCell (CellBlender) Properties Class:

class MCellPropertyGroup(bpy.types.PropertyGroup):
  # Note: should add one pointer property slot per GUI panel (like mol_viz).  Right now species list
  #   and active_mol_index are exposed here but should be grouped in a PropertyGroup.
  project_settings = bpy.props.PointerProperty(type=MCellProjectPanelProperty,name="CellBlender Project Settings")
  mol_viz = bpy.props.PointerProperty(type=MCellMolVizPanelProperty,name="Mol Viz Settings")
  species_list = bpy.props.CollectionProperty(type=MCellSpeciesProperty,name="Molecule List")
  active_mol_index = bpy.props.IntProperty(name="Active Molecule Index",default=0)
  reactions = bpy.props.PointerProperty(type=MCellReactionsPanelProperty,name="Defined Reactions")



# CellBlender Properties Class for Objects:

class MCellObjectPropertyGroup(bpy.types.PropertyGroup):
  regions = bpy.props.PointerProperty(type=MCellSurfaceRegionListProperty,name="Defined Surface Regions")



#CellBlender Operators:

class MCELL_OT_region_add(bpy.types.Operator):
  bl_idname = "mcell.region_add"
  bl_label = "Add New Surface Region"
  bl_description = "Add a new surface region to an object"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.object.mcell.regions.region_list.add()
    context.object.mcell.regions.active_reg_index = len(bpy.context.object.mcell.regions.region_list)-1
    return {'FINISHED'}
 


class MCELL_OT_region_remove(bpy.types.Operator):
  bl_idname = "mcell.region_remove"
  bl_label = "Remove Surface Region"
  bl_description = "Remove selected surface region from object"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.object.mcell.regions.region_list.remove(bpy.context.object.mcell.regions.active_reg_index)
    context.object.mcell.regions.active_reg_index = bpy.context.object.mcell.regions.active_reg_index-1
    if (context.object.mcell.regions.active_reg_index<0):
      context.object.mcell.regions.active_reg_index = 0
    return {'FINISHED'}



class MCELL_OT_region_faces_assign(bpy.types.Operator):
  bl_idname = "mcell.region_faces_assign"
  bl_label = "Assign Selected Faces To Surface Region"
  bl_description = "Assign selected faces to surface region"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    aobj = context.active_object
    obj_regs = aobj.mcell.regions
    if (aobj.data.total_face_sel > 0):
      if not aobj.data.get('mcell'):
        aobj.data['mcell'] = {}
      if not aobj.data['mcell'].get('regions'):
        aobj.data['mcell']['regions'] = {}
      reg = obj_regs.region_list[obj_regs.active_reg_index]
      if not aobj.data['mcell']['regions'].get(reg.name):
        aobj.data['mcell']['regions'][reg.name] = []
      mesh = aobj.data
      face_set = set([])
      for f in aobj.data['mcell']['regions'][reg.name]:
        face_set.add(f)
      bpy.ops.object.mode_set(mode='OBJECT')
      for f in mesh.faces:
        if f.select:
          face_set.add(f.index)
      bpy.ops.object.mode_set(mode='EDIT')

      reg_faces = list(face_set)
      reg_faces.sort()
      aobj.data['mcell']['regions'][reg.name] = reg_faces
          
#    obj_regs = aobj.mcell.regions
#    reg = obj_regs.region_list[obj_regs.active_reg_index]
#    mesh = aobj.data
#    for f in mesh.faces:
#      if f.select:
#        reg.faces.add()
#        reg.active_face_index = len(reg.faces)-1
#        reg.faces[reg.active_face_index].index = f.index
        
    return {'FINISHED'}
 


class MCELL_OT_region_faces_remove(bpy.types.Operator):
  bl_idname = "mcell.region_faces_remove"
  bl_label = "Remove Selected Faces From Surface Region"
  bl_description = "Remove selected faces from surface region"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    aobj = context.active_object
    obj_regs = aobj.mcell.regions
    if (aobj.data.total_face_sel > 0):
      if not aobj.data.get('mcell'):
        aobj.data['mcell'] = {}
      if not aobj.data['mcell'].get('regions'):
        aobj.data['mcell']['regions'] = {}
      reg = obj_regs.region_list[obj_regs.active_reg_index]
      if not aobj.data['mcell']['regions'].get(reg.name):
        aobj.data['mcell']['regions'][reg.name] = []
      mesh = aobj.data
      face_set = set(aobj.data['mcell']['regions'][reg.name].to_list())
      bpy.ops.object.mode_set(mode='OBJECT')
      for f in mesh.faces:
        if f.select:
          if f.index in face_set:
            face_set.remove(f.index)
      bpy.ops.object.mode_set(mode='EDIT')

      reg_faces = list(face_set)
      reg_faces.sort()
      aobj.data['mcell']['regions'][reg.name] = reg_faces

    return {'FINISHED'}
 


class MCELL_OT_region_faces_select(bpy.types.Operator):
  bl_idname = "mcell.region_faces_select"
  bl_label = "Select Faces of Selected Surface Region"
  bl_description = "Select faces of selected surface region"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    aobj = context.active_object
    obj_regs = aobj.mcell.regions
    if not aobj.data.get('mcell'):
      aobj.data['mcell'] = {}
    if not aobj.data['mcell'].get('regions'):
      aobj.data['mcell']['regions'] = {}
    reg = obj_regs.region_list[obj_regs.active_reg_index]
    if not aobj.data['mcell']['regions'].get(reg.name):
      aobj.data['mcell']['regions'][reg.name] = []
    mesh = aobj.data
    face_set = set(aobj.data['mcell']['regions'][reg.name].to_list())
    bpy.ops.object.mode_set(mode='OBJECT')
    for f in face_set:
      mesh.faces[f].select = True
    bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}
 


class MCELL_OT_region_faces_deselect(bpy.types.Operator):
  bl_idname = "mcell.region_faces_deselect"
  bl_label = "Deselect Faces of Selected Surface Region"
  bl_description = "Deselect faces of selected surface region"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    aobj = context.active_object
    obj_regs = aobj.mcell.regions
    if not aobj.data.get('mcell'):
      aobj.data['mcell'] = {}
    if not aobj.data['mcell'].get('regions'):
      aobj.data['mcell']['regions'] = {}
    reg = obj_regs.region_list[obj_regs.active_reg_index]
    if not aobj.data['mcell']['regions'].get(reg.name):
      aobj.data['mcell']['regions'][reg.name] = []
    mesh = aobj.data
    face_set = set(aobj.data['mcell']['regions'][reg.name].to_list())
    bpy.ops.object.mode_set(mode='OBJECT')
    for f in face_set:
      mesh.faces[f].select = False
    bpy.ops.object.mode_set(mode='EDIT')
    return {'FINISHED'}
 


class MCELL_OT_molecule_add(bpy.types.Operator):
  bl_idname = "mcell.molecule_add"
  bl_label = "Add Molecule"
  bl_description = "Add a new molecule type to an MCell model"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.scene.mcell.species_list.add()
    context.scene.mcell.active_mol_index = len(bpy.context.scene.mcell.species_list)-1
    return {'FINISHED'}
 


class MCELL_OT_molecule_remove(bpy.types.Operator):
  bl_idname = "mcell.molecule_remove"
  bl_label = "Remove Molecule"
  bl_description = "Remove selected molecule type from an MCell model"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.scene.mcell.species_list.remove(bpy.context.scene.mcell.active_mol_index)
    context.scene.mcell.active_mol_index = bpy.context.scene.mcell.active_mol_index-1
    if (context.scene.mcell.active_mol_index<0):
      context.scene.mcell.active_mol_index = 0
    return {'FINISHED'}



class MCELL_OT_reaction_add(bpy.types.Operator):
  bl_idname = "mcell.reaction_add"
  bl_label = "Add Reaction"
  bl_description = "Add a new reaction to an MCell model"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.scene.mcell.reactions.reaction_list.add()
    context.scene.mcell.reactions.active_rxn_index = len(bpy.context.scene.mcell.reactions.reaction_list)-1
    return {'FINISHED'}
 


class MCELL_OT_reaction_remove(bpy.types.Operator):
  bl_idname = "mcell.reaction_remove"
  bl_label = "Remove Reaction"
  bl_description = "Remove selected reaction from an MCell model"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    context.scene.mcell.reactions.reaction_list.remove(bpy.context.scene.mcell.reactions.active_rxn_index)
    context.scene.mcell.reactions.active_rxn_index = bpy.context.scene.mcell.reactions.active_rxn_index-1
    if (context.scene.mcell.reactions.active_rxn_index<0):
      context.scene.mcell.reactions.active_rxn_index = 0
    return {'FINISHED'}



class MCELL_OT_export_project(bpy.types.Operator):
  bl_idname = "mcell.export_project"
  bl_label = "Export CellBlender Project"
  bl_description = "Export CellBlender Project"
  bl_options = {'REGISTER'}
  
  def execute(self,context):
    mc = context.scene.mcell
    if mc.project_settings.export_format == 'mcell_mdl':
      if not mc.project_settings.export_selection_only:
        bpy.ops.object.select_by_type(type='MESH')
      filepath = mc.project_settings.project_dir+'/'+mc.project_settings.base_name+'.geometry.mdl'
      bpy.ops.export_mdl_mesh.mdl('INVOKE_DEFAULT',filepath=filepath)

    return {'FINISHED'}



class MCELL_OT_set_project_dir(bpy.types.Operator):
  bl_idname = "mcell.set_project_dir"
  bl_label = "Set CellBlender Project Directory"
  bl_description = "Set CellBlender Project Directory"
  bl_options = {'REGISTER','UNDO'}

  filepath = bpy.props.StringProperty(subtype="FILE_PATH")
  
  # Note: use classmethod "poll" to determine when runability of operator is valid
  #  @classmethod
  #  def poll(cls, context):
  #    return context.object is not None
  
  def execute(self, context):
    
    mc = context.scene.mcell
    if (os.path.isdir(self.filepath)):
      dir = self.filepath
    else:
      dir = os.path.dirname(self.filepath)
    
    # Reset mol_file_list to empty
    for i in range(mc.mol_viz.mol_file_num-1,-1,-1):
      mc.mol_viz.mol_file_list.remove(i)
    
    mc.project_settings.project_dir=dir
    return {'FINISHED'}
  
  def invoke(self, context, event):
    context.window_manager.fileselect_add(self)
    return {'RUNNING_MODAL'}



class MCELL_OT_set_mol_viz_dir(bpy.types.Operator):
  bl_idname = "mcell.set_mol_viz_dir"
  bl_label = "Read Molecule File"
  bl_description = "Read an MCell Molecule File for Visualization"
  bl_options = {'REGISTER'}

  filepath = bpy.props.StringProperty(subtype="FILE_PATH")
  
  # Note: use classmethod "poll" to determine when runability of operator is valid
  #  @classmethod
  #  def poll(cls, context):
  #    return context.object is not None
  
  def execute(self, context):
    
    mc = context.scene.mcell
    if (os.path.isdir(self.filepath)):
      mol_file_dir = self.filepath
    else:
      mol_file_dir = os.path.dirname(self.filepath)
    mol_file_list = glob.glob(mol_file_dir + '/*')
    mol_file_list.sort()
    
    # Reset mol_file_list to empty
    for i in range(mc.mol_viz.mol_file_num-1,-1,-1):
      mc.mol_viz.mol_file_list.remove(i)
    
    mc.mol_viz.mol_file_dir=mol_file_dir
    i = 0
    for mol_file_name in mol_file_list:
      new_item = mc.mol_viz.mol_file_list.add()
      new_item.name = os.path.basename(mol_file_name)
      i+=1
    
    mc.mol_viz.mol_file_num = len(mc.mol_viz.mol_file_list)
    mc.mol_viz.mol_file_stop_index = mc.mol_viz.mol_file_num-1
    mc.mol_viz.mol_file_index = 0
    
    MolVizUpdate(mc,0)
    return {'FINISHED'}
  
  def invoke(self, context, event):
    context.window_manager.fileselect_add(self)
    return {'RUNNING_MODAL'}



class MCELL_OT_mol_viz_set_index(bpy.types.Operator):
  bl_idname = "mcell.mol_viz_set_index"
  bl_label = "Set Molecule File Index"
  bl_description = "Set MCell Molecule File Index for Visualization"
  bl_options = {'REGISTER'}
  
  def execute(self,context):
    mc = bpy.data.scenes[0].mcell
    i = mc.mol_viz.mol_file_index
    if (i > mc.mol_viz.mol_file_stop_index):
      i = mc.mol_viz.mol_file_stop_index
    if (i < mc.mol_viz.mol_file_start_index):
      i = mc.mol_viz.mol_file_start_index
    mc.mol_viz.mol_file_index = i
    MolVizUpdate(mc,i)
    return{'FINISHED'}

#  def draw(self,context):
#    layout = self.layout

#    mc = context.scene.mcell
#    col = layout.col()
#    col.prop(mc.mol_viz,"mol_file_index",text="")



class MCELL_OT_mol_viz_next(bpy.types.Operator):
  bl_idname = "mcell.mol_viz_next"
  bl_label = "Step to Next Molecule File"
  bl_description = "Step to Next MCell Molecule File for Visualization"
  bl_options = {'REGISTER'}
  
  def execute(self,context):
    mc = context.scene.mcell
    i = mc.mol_viz.mol_file_index + mc.mol_viz.mol_file_step_index
    if (i > mc.mol_viz.mol_file_stop_index):
      i = mc.mol_viz.mol_file_stop_index
    mc.mol_viz.mol_file_index = i
    MolVizUpdate(mc,i)
    return{'FINISHED'}



class MCELL_OT_mol_viz_prev(bpy.types.Operator):
  bl_idname = "mcell.mol_viz_prev"
  bl_label = "Step to Previous Molecule File"
  bl_description = "Step to Previous MCell Molecule File for Visualization"
  bl_options = {'REGISTER'}
  
  def execute(self,context):
    mc = context.scene.mcell
    i = mc.mol_viz.mol_file_index - mc.mol_viz.mol_file_step_index
    if (i < mc.mol_viz.mol_file_start_index):
      i = mc.mol_viz.mol_file_start_index
    mc.mol_viz.mol_file_index = i
    MolVizUpdate(mc,i)
    return{'FINISHED'}



#CellBlender helper functions:

@persistent
def frame_change_handler(scn):
  mc = bpy.data.scenes[0].mcell
  curr_frame = mc.mol_viz.mol_file_index
  if (not curr_frame == scn.frame_current):
    mc.mol_viz.mol_file_index = scn.frame_current
    bpy.ops.mcell.mol_viz_set_index(None)
    scn.update()
    if mc.mol_viz.render_and_save:
      scn.render.filepath = '//stores_on/frames/frame_%05d.png' % (scn.frame_current)
      bpy.ops.render.render(write_still=True)



def render_handler(scn):
  mc = scn.mcell
  curr_frame = mc.mol_viz.mol_file_index
  if (not curr_frame == scn.frame_current):
    mc.mol_viz.mol_file_index = scn.frame_current
    bpy.ops.mcell.mol_viz_set_index(None)
  scn.update()



def MolVizUpdate(mcell_prop,i):
  mc = mcell_prop
  filename = mc.mol_viz.mol_file_list[i].name
  mc.mol_viz.mol_file_name = filename
  filepath = os.path.join(mc.mol_viz.mol_file_dir,filename)
  
  global_undo = bpy.context.user_preferences.edit.use_global_undo
  bpy.context.user_preferences.edit.use_global_undo = False
  
  MolVizUnlink(mc)
  MolVizFileRead(mc,filepath)
  
  bpy.context.user_preferences.edit.use_global_undo = global_undo



def MolVizDelete(mcell_prop):
  
  mc = mcell_prop
  bpy.ops.object.select_all(action='DESELECT')
  for mol_name in mc.mol_viz.mol_viz_list:
    bpy.ops.object.select_name(name=mol_name.name,extend=True)
  
  bpy.ops.object.delete('EXEC_DEFAULT')
  
  # Reset mol_viz_list to empty
  for i in range(len(mc.mol_viz.mol_viz_list)-1,-1,-1):
    mc.mol_viz.mol_viz_list.remove(i)



def MolVizUnlink(mcell_prop):
  
  mc = mcell_prop
  scn = bpy.data.scenes[0]
  scn_objs = scn.objects
  meshes = bpy.data.meshes
  objs = bpy.data.objects
  for mol_item in mc.mol_viz.mol_viz_list:
    mol_name = mol_item.name
    mol_obj = scn_objs[mol_name]
    scn_objs['%s_shape' % (mol_name)].parent = None
    mol_pos_mesh = mol_obj.data
    scn_objs.unlink(mol_obj)
    objs.remove(mol_obj)
  
  scn.update()
  # Reset mol_viz_list to empty
  for i in range(len(mc.mol_viz.mol_viz_list)-1,-1,-1):
    mc.mol_viz.mol_viz_list.remove(i)

    

def MolVizFileRead(mcell_prop,filepath):
  
  try:
    
#    begin = resource.getrusage(resource.RUSAGE_SELF)[0]
#    print ('Processing molecules from file:  %s' % (filepath))

    mol_data = [[s.split()[0], [float(x) for x in s.split()[1:]]] for s in open(filepath,'r').read().split('\n') if s != '']
    
    mols_obj = bpy.data.objects.get('molecules')
    if not mols_obj:
      bpy.ops.object.add()
      mols_obj = bpy.context.selected_objects[0]
      mols_obj.name = 'molecules'
    
    if len(mol_data) > 0:
      meshes = bpy.data.meshes
      mats = bpy.data.materials
      objs = bpy.data.objects
      scn = bpy.data.scenes[0]
      scn_objs = scn.objects
      mc = mcell_prop
      z_axis = mathutils.Vector((0.0, 0.0, 1.0))
      ident_mat = mathutils.Matrix.Translation(mathutils.Vector((0.0,0.0,0.0)))
      
      mol_dict = {}
      mol_pos = []
      mol_orient = []
      
      for n in range(len(mol_data)):
        mol_name = 'mol_%s' % (mol_data[n][0])
        if not mol_dict.get(mol_name):
          mol_dict[mol_name] = [[],[]]
          new_item = mc.mol_viz.mol_viz_list.add()
          new_item.name = mol_name
        mol_dict[mol_name][0].extend(mol_data[n][1][0:3])
        mol_dict[mol_name][1].extend(mol_data[n][1][3:])
      
      for mol_name in mol_dict.keys():
        mol_mat_name='%s_mat'%(mol_name)
        mol_pos = mol_dict[mol_name][0]
        mol_orient = mol_dict[mol_name][1]

#       Name mesh shape template according to molecule type (2D or 3D)
#         TODO: we can now use shape from molecule properties if it exists
        if (mol_orient[0] != 0.0) | (mol_orient[1] != 0.0) | (mol_orient[2] != 0.0):
          is_vmol = False
          mol_shape_mesh_name = '%s_shape' % (mol_name)
          mol_shape_obj_name = mol_shape_mesh_name
        else:
          is_vmol = True
          mol_shape_mesh_name = '%s_shape' % (mol_name)
          mol_shape_obj_name = mol_shape_mesh_name
          for n in range(len(mol_orient)):
            mol_orient[n] = random.uniform(-1.0,1.0)

#       Look-up mesh shape template and create if needed
        mol_shape_mesh = meshes.get(mol_shape_mesh_name)
        if not mol_shape_mesh:
          bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=0, size=0.01)
          mol_shape_obj = bpy.context.active_object
          mol_shape_obj.name = mol_shape_obj_name
          mol_shape_obj.track_axis = "POS_Z" 
          mol_shape_mesh = mol_shape_obj.data
          mol_shape_mesh.name = mol_shape_mesh_name
        else:
          mol_shape_obj = objs.get(mol_shape_obj_name)
      

#       Look-up material and create if needed. Associate material with mesh shape
        mol_mat = mats.get(mol_mat_name)
        if not mol_mat:
          mol_mat = mats.new(mol_mat_name)
          mol_mat.diffuse_color = [1.0, 0.0, 0.0]
        if not mol_shape_mesh.materials.get(mol_mat_name):
          mol_shape_mesh.materials.append(mol_mat)
#       Create mol mesh to hold molecule positions
        mol_pos_mesh_name = '%s_pos' % (mol_name)
        mol_pos_mesh = meshes.get(mol_pos_mesh_name)
        if mol_pos_mesh:
          meshes.remove(mol_pos_mesh)
        
        mol_pos_mesh = meshes.new(mol_pos_mesh_name)
        mol_pos_mesh.vertices.add(len(mol_pos)//3)
        mol_pos_mesh.vertices.foreach_set("co",mol_pos)
        mol_pos_mesh.vertices.foreach_set("normal",mol_orient)
        
        mol_obj = objs.get(mol_name)
        if not mol_obj:
          mol_obj = objs.new(mol_name,mol_pos_mesh)
        if not scn_objs.get(mol_name):
          scn_objs.link(mol_obj)
        
        mol_shape_obj.parent = mol_obj
        mol_obj.dupli_type = 'VERTS'
        mol_obj.use_dupli_vertices_rotation=True
        mol_obj.parent = mols_obj
          
    scn.update()

#    utime = resource.getrusage(resource.RUSAGE_SELF)[0]-begin
#    print ('   Processed %d molecules in %g seconds\n' % (len(mol_data),utime))

  except IOError:
    print(('\n***** File not found: %s\n') % (filepath))
  except ValueError:
    print(('\n***** Invalid data in file: %s\n') % (filepath))



def register():
  bpy.utils.register_class(MCellSpeciesProperty)
  bpy.utils.register_class(MCellReactionProperty)
  bpy.utils.register_class(MCellStringProperty)
  bpy.utils.register_class(MCellProjectPanelProperty)
  bpy.utils.register_class(MCellMolVizPanelProperty)
  bpy.utils.register_class(MCellReactionsPanelProperty)
  bpy.utils.register_class(MCellPropertyGroup)
  bpy.types.Scene.mcell = bpy.props.PointerProperty(type=MCellPropertyGroup)

  bpy.utils.register_class(MCellSurfaceRegionFaceProperty)
  bpy.utils.register_class(MCellSurfaceRegionProperty)
  bpy.utils.register_class(MCellSurfaceRegionListProperty)
  bpy.utils.register_class(MCellObjectPropertyGroup)
  bpy.types.Object.mcell = bpy.props.PointerProperty(type=MCellObjectPropertyGroup)

  bpy.utils.register_class(MCELL_OT_set_project_dir)
  bpy.utils.register_class(MCELL_OT_export_project)
  bpy.utils.register_class(MCELL_OT_set_mol_viz_dir)
  bpy.utils.register_class(MCELL_OT_region_add)
  bpy.utils.register_class(MCELL_OT_region_remove)
  bpy.utils.register_class(MCELL_OT_region_faces_assign)
  bpy.utils.register_class(MCELL_OT_region_faces_remove)
  bpy.utils.register_class(MCELL_OT_region_faces_select)
  bpy.utils.register_class(MCELL_OT_region_faces_deselect)
  bpy.utils.register_class(MCELL_OT_molecule_add)
  bpy.utils.register_class(MCELL_OT_molecule_remove)
  bpy.utils.register_class(MCELL_OT_reaction_add)
  bpy.utils.register_class(MCELL_OT_reaction_remove)
  bpy.utils.register_class(MCELL_OT_mol_viz_set_index)
  bpy.utils.register_class(MCELL_OT_mol_viz_next)
  bpy.utils.register_class(MCELL_OT_mol_viz_prev)
  bpy.utils.register_class(MCELL_PT_project_settings)
  bpy.utils.register_class(MCELL_PT_sim_control)
  bpy.utils.register_class(MCELL_PT_viz_results)
  bpy.utils.register_class(MCELL_PT_utilities)
  bpy.utils.register_class(MCELL_PT_user_model_parameters)
  bpy.utils.register_class(MCELL_PT_initialization)
  bpy.utils.register_class(MCELL_PT_define_molecules)
  bpy.utils.register_class(MCELL_PT_define_reactions)
  bpy.utils.register_class(MCELL_PT_define_surface_classes)
  bpy.utils.register_class(MCELL_PT_define_surface_regions)
  bpy.utils.register_class(MCELL_PT_molecule_placement)
  bpy.utils.register_class(MCELL_PT_reaction_output_settings)
  bpy.utils.register_class(MCELL_PT_visualization_output_settings)


def unregister():
#  del bpy.types.Scene.mcell
  pass
      

if len(bpy.app.handlers.frame_change_pre) == 0:
  bpy.app.handlers.frame_change_pre.append(frame_change_handler)

if __name__ == '__main__':
  register()
#  bpy.app.handlers.frame_change_pre.append(frame_change_handler)
#  bpy.app.handlers.render_pre.append(render_handler)
#  bpy.app.handlers.render_pre.append(frame_change_handler)


# Notes:
#   template_list takes a CollectionProperty and active index as input
#     "name" member of each item in the collection is shown in the GUI
#     the item specified by active index is highlighted

#   Turn off global undo for better performance and atomic operation of sequence of operators:
#     bpy.context.user_preferences.edit.use_global_undo = False
#     ...
#     bpy.context.user_preferences.edit.use_global_undo = True