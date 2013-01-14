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


import bpy
from . import cellblender_operators
from bpy.props import CollectionProperty, EnumProperty, FloatProperty, IntProperty, StringProperty


#Custom Properties

class MCellSurfaceRegionFaceProperty(bpy.types.PropertyGroup):
  index = bpy.props.IntProperty(name="Face Index")


class MCellSurfaceRegionProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Region Name",default="Region",update=cellblender_operators.check_region)
  faces = bpy.props.CollectionProperty(type=MCellSurfaceRegionFaceProperty,name="Surface Region List")
  active_face_index = bpy.props.IntProperty(name="Active Face Index",default=0)


class MCellSurfaceRegionListProperty(bpy.types.PropertyGroup):
  region_list = bpy.props.CollectionProperty(type=MCellSurfaceRegionProperty,name="Surface Region List")
  active_reg_index = bpy.props.IntProperty(name="Active Region Index",default=0)
  status = bpy.props.StringProperty(name="Status")


class MCellMoleculeProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Molecule Name",default="Molecule",update=cellblender_operators.check_molecule)
  type_enum = [
                    ('2D','Surface Molecule',''),
                    ('3D','Volume Molecule','')]
  type = bpy.props.EnumProperty(items=type_enum,name="Molecule Type")
  diffusion_constant = bpy.props.FloatProperty(name="Diffusion Constant")
  diffusion_constant_str = bpy.props.StringProperty(name="Diffusion Constant",description="Diffusion Constant Units: cm^2/sec",update=cellblender_operators.update_diffusion_constant)
  target_only = bpy.props.BoolProperty(name="Target Only")
  custom_time_step = bpy.props.FloatProperty(name="Custom Time Step")
  custom_time_step_str = bpy.props.StringProperty(name="Custom Time Step",description="Custom Time Step Units: seconds",update=cellblender_operators.update_custom_time_step)
  custom_space_step = bpy.props.FloatProperty(name="Custom Space Step")
  custom_space_step_str = bpy.props.StringProperty(name="Custom Space Step",description="Custom Space Step Units: microns",update=cellblender_operators.update_custom_space_step)
  

# Generic PropertyGroup to hold strings for a ColletionProperty  
class MCellStringProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Text")


# Generic PropertyGroup to hold float vectors for a ColletionProperty  
class MCellFloatVectorProperty(bpy.types.PropertyGroup):
  vec = bpy.props.FloatVectorProperty(name="Float Vector")


class MCellReactionProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="The Reaction")
  rxn_name = bpy.props.StringProperty(name="Reaction Name")
  reactants = bpy.props.StringProperty(name="Reactants",update=cellblender_operators.check_reaction)
  products = bpy.props.StringProperty(name="Products",update=cellblender_operators.check_reaction)
  type_enum = [
                ('irreversible','->',''),
                ('reversible','<->','')]
  type = bpy.props.EnumProperty(items=type_enum,name="Reaction Type",update=cellblender_operators.check_reaction)
  fwd_rate = bpy.props.FloatProperty(name="Forward Rate")
  fwd_rate_str = bpy.props.StringProperty(name="Forward Rate",description="Forward Rate Units: sec^-1 (unimolecular), M^-1*sec^-1 (bimolecular)",update=cellblender_operators.update_fwd_rate)
  bkwd_rate = bpy.props.FloatProperty(name="Backward Rate")
  bkwd_rate_str = bpy.props.StringProperty(name="Backward Rate",description="Backward Rate Units: sec^-1 (unimolecular), M^-1*sec^-1 (bimolecular)",update=cellblender_operators.update_bkwd_rate)


class MCellMoleculeReleaseProperty(bpy.types.PropertyGroup):
  name = bpy.props.StringProperty(name="Site Name",default="Release_Site",update=cellblender_operators.check_release_site)
  molecule = bpy.props.StringProperty(name="Molecule",update=cellblender_operators.check_release_molecule)
  shape_enum = [
                ('CUBIC','Cubic',''),
                ('SPHERICAL','Spherical',''),
                ('SPHERICAL SHELL','Spherical Shell',''),
  #              ('LIST','List',''),
                ('OBJECT','Object/Region','')]
  shape = bpy.props.EnumProperty(items=shape_enum,name="Release Shape")
  object_expr = bpy.props.StringProperty(name="Object/Region",update=cellblender_operators.check_release_object_expr)
  location = bpy.props.FloatVectorProperty(name="Location",precision=4)
  diameter = bpy.props.FloatProperty(name="Site Diameter",precision=4,min=0.0)
  probability = bpy.props.FloatProperty(name="Release Probability",precision=4,default=1.0,min=0.0,max=1.0)
  quantity_type_enum = [
                ('NUMBER_TO_RELEASE','Constant Number',''),
                ('GAUSSIAN_RELEASE_NUMBER','Gaussian Number',''),
                ('DENSITY','Concentration/Density','')]
  quantity_type = bpy.props.EnumProperty(items=quantity_type_enum,name="Quantity Type")
  quantity = bpy.props.FloatProperty(name="Quantity to Release",precision=4,min=0.0)
  stddev = bpy.props.FloatProperty(name="Standard Deviation",precision=4,min=0.0)
  pattern = bpy.props.StringProperty(name="Release Pattern")


class MCellSurfaceClassPropertiesProperty(bpy.types.PropertyGroup):
    """This is where properties for a given surface class are stored

    All of the properties here ultimately get converted into something like the
    following: ABSORPTIVE = Molecule' or REFLECTIVE = Molecule;
    Each instance is only one set of properties for a surface class that may
    have many sets of properties

    """
    name = StringProperty(name="Molecule", default="Molecule")
    molecule = StringProperty(
        name="Molecule Name:",
        update=cellblender_operators.check_surf_class_props)
    surf_class_orient_enum = [
        ("'", 'Top/Front', ''),
        (",", 'Bottom/Back', ''),
        (";", 'Ignore', '')]
    surf_class_orient = EnumProperty(
        items=surf_class_orient_enum, name="Orientation",
        update=cellblender_operators.check_surf_class_props)
    surf_class_type_enum = [
        ('ABSORPTIVE', 'Absorptive', ''),
        ('TRANSPARENT', 'Transparent', ''),
        ('REFLECTIVE', 'Reflective', ''),
        ('CLAMP_CONCENTRATION', 'Clamp Concentration', '')]
    surf_class_type = EnumProperty(
        items=surf_class_type_enum, name="Type",
        update=cellblender_operators.check_surf_class_props)
    clamp_value = FloatProperty(name="Value", precision=4, min=0.0)
    clamp_value_str = StringProperty(
        name="Value", description="Concentration Units: Molar",
        update=cellblender_operators.update_clamp_value)


class MCellSurfaceClassesProperty(bpy.types.PropertyGroup):
    """Stores the surface class name and a list of its properties"""

    name = StringProperty(name="Surface Class Name", default="Surface_Class",
                          update=cellblender_operators.check_surface_class)
    surf_class_props_list = CollectionProperty(
        type=MCellSurfaceClassPropertiesProperty, name="Surface Classes List")
    active_surf_class_props_index = IntProperty(
        name="Active Surface Class Index", default=0)


class MCellModSurfRegionsProperty(bpy.types.PropertyGroup):
    """Assign a surface class to a surface region"""

    name = StringProperty(name="Surface Class Name", default="Surface_Class")
    surf_class_name = StringProperty(
        name="Surface Class Name:",
        update=cellblender_operators.check_assigned_surface_class)
    object_name = StringProperty(
        name="Object Name:",
        update=cellblender_operators.check_assigned_object)
    region_name = StringProperty(
        name="Region Name:",
        update=cellblender_operators.check_modified_region)


#Panel Properties:

class MCellProjectPanelProperty(bpy.types.PropertyGroup):
  base_name = bpy.props.StringProperty(name="Project Base Name")
  project_dir = bpy.props.StringProperty(name="Project Directory")
  export_format_enum = [
                         ('mcell_mdl_unified','Single Unified MCell MDL File',''),
                         ('mcell_mdl_modular','Modular MCell MDL Files','')]
  export_format = bpy.props.EnumProperty(items=export_format_enum,name="Export Format",default="mcell_mdl_modular")
#  export_selection_only = bpy.props.BoolProperty(name="Export Selected Objects Only",default=True)


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
  mol_viz_enable = bpy.props.BoolProperty(name="Enable Molecule Vizualization",description="Disable for faster animation preview",default=True,update=cellblender_operators.MolVizUpdate)
  color_list = bpy.props.CollectionProperty(type=MCellFloatVectorProperty,name="Molecule Color List")
  color_index = bpy.props.IntProperty(name="Color Index",default=0)


class MCellInitializationPanelProperty(bpy.types.PropertyGroup):
  iterations = bpy.props.IntProperty(name="Simulation Iterations",description="Number of Iterations to Run",default=0,min=0)
  time_step = bpy.props.FloatProperty(name="Time Step",default=1e-6,min=0.0)
  time_step_str = bpy.props.StringProperty(name="Time Step",default="1e-6",description="Simulation Time Step Units: seconds",update=cellblender_operators.update_time_step)
  status = bpy.props.StringProperty(name="Status")


class MCellMoleculesPanelProperty(bpy.types.PropertyGroup):
  molecule_list = bpy.props.CollectionProperty(type=MCellMoleculeProperty,name="Molecule List")
  active_mol_index = bpy.props.IntProperty(name="Active Molecule Index",default=0)
  status = bpy.props.StringProperty(name="Status")


class MCellReactionsPanelProperty(bpy.types.PropertyGroup):
  reaction_list = bpy.props.CollectionProperty(type=MCellReactionProperty,name="Reaction List")
  active_rxn_index = bpy.props.IntProperty(name="Active Reaction Index",default=0)
  status = bpy.props.StringProperty(name="Status")


class MCellSurfaceClassesPanelProperty(bpy.types.PropertyGroup):
    surf_class_list = CollectionProperty(type=MCellSurfaceClassesProperty,
                                         name="Surface Classes List")
    active_surf_class_index = IntProperty(name="Active Surface Class Index",
                                          default=0)
    surf_class_status = bpy.props.StringProperty(name="Status")
    surf_class_props_status = bpy.props.StringProperty(name="Status")


class MCellModSurfRegionsPanelProperty(bpy.types.PropertyGroup):
    mod_surf_regions_list = CollectionProperty(
        type=MCellModSurfRegionsProperty, name="Modify Surface Region List")
    active_mod_surf_regions_index = IntProperty(
        name="Active Modify Surface Region Index", default=0)
    status = bpy.props.StringProperty(name="Status")


class MCellMoleculeReleasePanelProperty(bpy.types.PropertyGroup):
  mol_release_list = bpy.props.CollectionProperty(type=MCellMoleculeReleaseProperty,name="Molecule Release List")
  active_release_index = bpy.props.IntProperty(name="Active Release Index",default=0)
  status = bpy.props.StringProperty(name="Status")


class MCellModelObjectsPanelProperty(bpy.types.PropertyGroup):
  object_list = bpy.props.CollectionProperty(type=MCellStringProperty,name="Object List")
  active_obj_index = bpy.props.IntProperty(name="Active Object Index",default=0)


class MCellVizOutputPanelProperty(bpy.types.PropertyGroup):
  include = bpy.props.BoolProperty(name="Include Viz Output",description="Add INCLUDE_FILE for Viz Output to main MDL file",default=False)


class MCellReactionOutputPanelProperty(bpy.types.PropertyGroup):
  include = bpy.props.BoolProperty(name="Include Reaction Output",description="Add INCLUDE_FILE for Reaction Output to main MDL file",default=False)


class MCellMoleculeGlyphsPanelProperty(bpy.types.PropertyGroup):
  glyph_lib = __file__.replace(__file__.split('/')[len(__file__.split('/'))-1],'')+'glyph_library.blend/Mesh/'
  glyph_enum = [
                    ('Cone','Cone',''),
                    ('Cube','Cube',''),
                    ('Cylinder','Cylinder',''),
                    ('Icosahedron','Icosahedron',''),
                    ('Octahedron','Octahedron',''),
                    ('Receptor','Receptor',''),
                    ('Sphere_1','Sphere_1',''),
                    ('Sphere_2','Sphere_2',''),
                    ('Torus','Torus','')]
  glyph = bpy.props.EnumProperty(items=glyph_enum,name="Molecule Shapes")
  status = bpy.props.StringProperty(name="Status")


class MCellMeshalyzerPanelProperty(bpy.types.PropertyGroup):
  object_name = bpy.props.StringProperty(name="Object Name")
  vertices = bpy.props.IntProperty(name="Vertices",default=0)
  edges = bpy.props.IntProperty(name="Edges",default=0)
  faces = bpy.props.IntProperty(name="Faces",default=0)
  watertight = bpy.props.StringProperty(name="Watertight")
  manifold = bpy.props.StringProperty(name="Manifold")
  normal_status = bpy.props.StringProperty(name="Surface Normals")
  area = bpy.props.FloatProperty(name="Area",default=0)
  volume = bpy.props.FloatProperty(name="Volume",default=0)
  status = bpy.props.StringProperty(name="Status")


class MCellObjectSelectorPanelProperty(bpy.types.PropertyGroup):
  filter = bpy.props.StringProperty(name="Object Name Filter")


# Main MCell (CellBlender) Properties Class:

class MCellPropertyGroup(bpy.types.PropertyGroup):
  project_settings = bpy.props.PointerProperty(type=MCellProjectPanelProperty,name="CellBlender Project Settings")
  mol_viz = bpy.props.PointerProperty(type=MCellMolVizPanelProperty,name="Mol Viz Settings")
  initialization = bpy.props.PointerProperty(type=MCellInitializationPanelProperty,name="Model Initialization")
  molecules = bpy.props.PointerProperty(type=MCellMoleculesPanelProperty,name="Defined Molecules")
  reactions = bpy.props.PointerProperty(type=MCellReactionsPanelProperty,name="Defined Reactions")
  surface_classes = bpy.props.PointerProperty(type=MCellSurfaceClassesPanelProperty,name="Defined Surface Classes")
  mod_surf_regions = bpy.props.PointerProperty(type=MCellModSurfRegionsPanelProperty,name="Modify Surface Regions")
  release_sites = bpy.props.PointerProperty(type=MCellMoleculeReleasePanelProperty,name="Defined Release Sites")
  model_objects = bpy.props.PointerProperty(type=MCellModelObjectsPanelProperty,name="Instantiated Objects")
  viz_output = bpy.props.PointerProperty(type=MCellVizOutputPanelProperty,name="Viz Output")
  rxn_output = bpy.props.PointerProperty(type=MCellReactionOutputPanelProperty,name="Reaction Output")
  meshalyzer = bpy.props.PointerProperty(type=MCellMeshalyzerPanelProperty,name="CellBlender Project Settings")
  object_selector = bpy.props.PointerProperty(type=MCellObjectSelectorPanelProperty,name="CellBlender Project Settings")
  molecule_glyphs = bpy.props.PointerProperty(type=MCellMoleculeGlyphsPanelProperty,name="Molecule Shapes")



# CellBlender Properties Class for Objects:

class MCellObjectPropertyGroup(bpy.types.PropertyGroup):
  regions = bpy.props.PointerProperty(type=MCellSurfaceRegionListProperty,name="Defined Surface Regions")
  status = bpy.props.StringProperty(name="Status")


