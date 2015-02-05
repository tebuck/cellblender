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
This script contains the custom properties used in CellBlender.

"""
# blender imports
import bpy
from . import cellblender_operators
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, PointerProperty, StringProperty

from . import cellblender_molecules
from . import parameter_system

# python imports
from multiprocessing import cpu_count


# we use per module class registration/unregistration
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


#Custom Properties

class MCellStringProperty(bpy.types.PropertyGroup):
    """ Generic PropertyGroup to hold string for a CollectionProperty """
    name = StringProperty(name="Text")


class MCellFloatVectorProperty(bpy.types.PropertyGroup):
    """ Generic PropertyGroup to hold float vector for a CollectionProperty """
    vec = bpy.props.FloatVectorProperty(name="Float Vector")


class MCellReactionProperty(bpy.types.PropertyGroup):
    name = StringProperty(name="The Reaction")
    rxn_name = StringProperty(
        name="Reaction Name",
        description="The name of the reaction. "
                    "Can be used in Reaction Output.",
        update=cellblender_operators.update_release_pattern_rxn_name_list)
    reactants = StringProperty(
        name="Reactants", 
        description="Specify 1-3 reactants separated by a + symbol. "
                    "Optional: end with @ surface class. Ex: a; + b; @ sc;",
        update=cellblender_operators.check_reaction)
    products = StringProperty(
        name="Products",
        description="Specify zero(NULL) or more products separated by a + "
                    "symbol.",
        update=cellblender_operators.check_reaction)
    type_enum = [
        ('irreversible', "->", ""),
        ('reversible', "<->", "")]
    type = EnumProperty(
        items=type_enum, name="Reaction Type",
        description="A unidirectional/irreversible(->) reaction or a "
                    "bidirectional/reversible(<->) reaction.",
        update=cellblender_operators.check_reaction)
    variable_rate_switch = BoolProperty(
        name="Enable Variable Rate Constant",
        description="If set, use a variable rate constant defined by a two "
                    "column file (col1=time, col2=rate).",
        default=False, update=cellblender_operators.check_reaction)
    variable_rate = StringProperty(
        name="Variable Rate", subtype='FILE_PATH', default="")
    variable_rate_valid = BoolProperty(name="Variable Rate Valid",
        default=False, update=cellblender_operators.check_reaction)


    fwd_rate = PointerProperty ( name="Forward Rate", type=parameter_system.Parameter_Reference )
    bkwd_rate = PointerProperty ( name="Forward Rate", type=parameter_system.Parameter_Reference )


    def init_properties ( self, parameter_system ):
        self.fwd_rate.init_ref   ( parameter_system, "FW_Rate_Type", user_name="Forward Rate",  user_expr="0", user_units="",  user_descr="Forward Rate" )
        self.bkwd_rate.init_ref  ( parameter_system, "BW_Rate_Type", user_name="Backward Rate", user_expr="",  user_units="s", user_descr="Backward Rate" )

    status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        r = self
        r_dict = {}
        r_dict['name'] = r.name
        r_dict['rxn_name'] = r.rxn_name
        r_dict['reactants'] = r.reactants
        r_dict['products'] = r.products
        r_dict['rxn_type'] = r.type
        r_dict['variable_rate_switch'] = r.variable_rate_switch
        r_dict['variable_rate'] = r.variable_rate
        r_dict['variable_rate_valid'] = r.variable_rate_valid
        r_dict['fwd_rate'] = r.fwd_rate.get_expr()
        r_dict['bkwd_rate'] = r.bkwd_rate.get_expr()
        variable_rate_text = ""
        if r.type == 'irreversible':
            # Check if a variable rate constant file is specified
            if r.variable_rate_switch and r.variable_rate_valid:
                variable_rate_text = bpy.data.texts[r.variable_rate].as_string()
        r_dict['variable_rate_text'] = variable_rate_text
        return r_dict



class MCellMoleculeReleaseProperty(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Site Name", default="Release_Site",
        description="The name of the release site",
        update=cellblender_operators.check_release_site)
    molecule = StringProperty(
        name="Molecule",
        description="The molecule to release",
        update=cellblender_operators.check_release_site)
    shape_enum = [
        ('CUBIC', 'Cubic', ''),
        ('SPHERICAL', 'Spherical', ''),
        ('SPHERICAL_SHELL', 'Spherical Shell', ''),
        #('LIST', 'List', ''),
        ('OBJECT', 'Object/Region', '')]
    shape = EnumProperty(
        items=shape_enum, name="Release Shape",
        description="Release in the specified shape. Surface molecules can "
                    "only use Object/Region.",
                    update=cellblender_operators.check_release_site)
    orient_enum = [
        ('\'', "Top Front", ""),
        (',', "Top Back", ""),
        (';', "Mixed", "")]
    orient = bpy.props.EnumProperty(
        items=orient_enum, name="Initial Orientation",
        description="Release surface molecules with the specified initial "
                    "orientation.")
    object_expr = StringProperty(
        name="Object/Region",
        description="Release in/on the specified object/region.",
        update=cellblender_operators.check_release_site)
    location = bpy.props.FloatVectorProperty(
        name="Location", precision=4,
        description="The center of the release site specified by XYZ "
                    "coordinates")

    location_x = PointerProperty ( name="Relese Loc X", type=parameter_system.Parameter_Reference )
    location_y = PointerProperty ( name="Relese Loc Y", type=parameter_system.Parameter_Reference )
    location_z = PointerProperty ( name="Relese Loc Z", type=parameter_system.Parameter_Reference )

    diameter = PointerProperty ( name="Site Diameter", type=parameter_system.Parameter_Reference )
    probability = PointerProperty ( name="Release Probability", type=parameter_system.Parameter_Reference )

    quantity_type_enum = [
        ('NUMBER_TO_RELEASE', "Constant Number", ""),
        ('GAUSSIAN_RELEASE_NUMBER', "Gaussian Number", ""),
        ('DENSITY', "Concentration/Density", "")]
    quantity_type = EnumProperty(items=quantity_type_enum,
                                 name="Quantity Type")

    quantity = PointerProperty ( name="Quantity to Release", type=parameter_system.Parameter_Reference )
    stddev = PointerProperty ( name="Standard Deviation", type=parameter_system.Parameter_Reference )

    pattern = StringProperty(
        name="Release Pattern",
        description="Use the named release pattern. "
                    "If blank, release molecules at start of simulation.")
    status = StringProperty(name="Status")

    def init_properties ( self, parameter_system ):
        self.diameter.init_ref    ( parameter_system, "Diam_Type",       user_name="Site Diameter",       user_expr="0", user_units="", user_descr="Release molecules uniformly within the specified diameter." )
        self.probability.init_ref ( parameter_system, "Rel_Prob_Type",   user_name="Release Probability", user_expr="1", user_units="", user_descr="Release does not occur every time,\nbut rather with specified probability." )
        self.quantity.init_ref    ( parameter_system, "Rel_Quant_Type",  user_name="Quantity to Release", user_expr="",  user_units="", user_descr="Concentration units: molar. Density units: molecules per square micron" )
        self.stddev.init_ref      ( parameter_system, "Rel_StdDev_Type", user_name="Standard Deviation",  user_expr="0", user_units="", user_descr="Standard Deviation" )
        self.location_x.init_ref  ( parameter_system, "Rel_Loc_Type_X",  user_name="Release Location X",  user_expr="0", user_units="", user_descr="The center of the release site's X coordinate" )
        self.location_y.init_ref  ( parameter_system, "Rel_Loc_Type_Y",  user_name="Release Location Y",  user_expr="0", user_units="", user_descr="The center of the release site's Y coordinate" )
        self.location_z.init_ref  ( parameter_system, "Rel_Loc_Type_Z",  user_name="Release Location Z",  user_expr="0", user_units="", user_descr="The center of the release site's Z coordinate" )

    def build_data_model_from_properties ( self, context ):
        r = self
        r_dict = {}
        r_dict['name'] = r.name
        r_dict['molecule'] = r.molecule
        r_dict['shape'] = r.shape
        r_dict['orient'] = r.orient
        r_dict['object_expr'] = r.object_expr
        r_dict['location_x'] = r.location_x.get_expr()
        r_dict['location_y'] = r.location_y.get_expr()
        r_dict['location_z'] = r.location_z.get_expr()
        r_dict['site_diameter'] = r.diameter.get_expr()
        r_dict['release_probability'] = r.probability.get_expr()
        r_dict['quantity_type'] = str(r.quantity_type)
        r_dict['quantity'] = r.quantity.get_expr()
        r_dict['stddev'] = r.stddev.get_expr()
        r_dict['pattern'] = str(r.pattern)
        return r_dict


class MCellReleasePatternProperty(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Site Name", default="Release_Site",
        description="The name of the release site",
        update=cellblender_operators.check_release_pattern_name)

    """
    delay = FloatProperty(name="Delay")
    delay_str = StringProperty(
        name="Delay",
        default="0",
        description="The time at which the release pattern will start "
                    "(units: seconds).",
        update=cellblender_operators.update_delay)

    release_interval = FloatProperty(name="Release Interval", default=1e-12)
    release_interval_str = StringProperty(
        name="Release Interval",
        default="1e-12",
        description="During a train, release molecules after every interval "
                    "(units: seconds). Default is once.",
        update=cellblender_operators.update_release_interval)

    train_duration = FloatProperty(name="Train Duration", default=1e-12)
    train_duration_str = StringProperty(
        name="Train Duration",
        default="1e-12",
        description="The duration of the train before turning off "
                    "(units: seconds). Default is to never turn off.",
        update=cellblender_operators.update_train_duration)

    train_interval = FloatProperty(name="Train Interval", default=1e-12)
    train_interval_str = StringProperty(
        name="Train Interval",
        default="1e-12",
        description="A new train happens every interval (units: seconds). "
                    "Default is no new trains.",
        update=cellblender_operators.update_train_interval)

    number_of_trains = IntProperty(
        name="Number of Trains", min=0,
        description="Repeat the release process this number of times. "
                    "Default is one train.")
    """

    delay            = PointerProperty ( name="Release Pattern Delay", type=parameter_system.Parameter_Reference )
    release_interval = PointerProperty ( name="Relese Interval",       type=parameter_system.Parameter_Reference )
    train_duration   = PointerProperty ( name="Train Duration",        type=parameter_system.Parameter_Reference )
    train_interval   = PointerProperty ( name="Train Interval",        type=parameter_system.Parameter_Reference )
    number_of_trains = PointerProperty ( name="Number of Trains",      type=parameter_system.Parameter_Reference )

    status = StringProperty(name="Status")

    def init_properties ( self, parameter_system ):
        self.delay.init_ref            ( parameter_system, "Rel_Delay_Type", user_name="Release Pattern Delay", user_expr="0",     user_units="s", user_descr="The time at which the release pattern will start." )
        self.release_interval.init_ref ( parameter_system, "Rel_Int_Type",   user_name="Relese Interval",       user_expr="1e-12", user_units="s", user_descr="During a train, release molecules after every interval.\nDefault is once." )
        self.train_duration.init_ref   ( parameter_system, "Tr_Dur_Type",    user_name="Train Duration",        user_expr="1e-12", user_units="s", user_descr="The duration of the train before turning off.\nDefault is to never turn off." )
        self.train_interval.init_ref   ( parameter_system, "Tr_Int_Type",    user_name="Train Interval",        user_expr="1e-12", user_units="s", user_descr="A new train happens every interval.\nDefault is no new trains." )
        self.number_of_trains.init_ref ( parameter_system, "NTrains_Type",   user_name="Number of Trains",      user_expr="0",     user_units="",  user_descr="Repeat the release process this number of times.\nDefault is one train.", user_int=True )

    def build_data_model_from_properties ( self, context ):
        r = self
        r_dict = {}
        r_dict['name'] = r.name
        r_dict['delay'] = r.delay.get_expr()
        r_dict['release_interval'] = r.release_interval.get_expr()
        r_dict['train_duration'] = r.train_duration.get_expr()
        r_dict['train_interval'] = r.train_interval.get_expr()
        r_dict['number_of_trains'] = r.number_of_trains.get_expr()
        return r_dict


class MCellSurfaceClassPropertiesProperty(bpy.types.PropertyGroup):

    """ This is where properties for a given surface class are stored.

    All of the properties here ultimately get converted into something like the
    following: ABSORPTIVE = Molecule' or REFLECTIVE = Molecule;
    Each instance is only one set of properties for a surface class that may
    have many sets of properties.

    """

    name = StringProperty(name="Molecule", default="Molecule")
    molecule = StringProperty(
        name="Molecule Name",
        description="The molecule that is affected by the surface class",
        update=cellblender_operators.check_surf_class_props)
    surf_class_orient_enum = [
        ('\'', "Top/Front", ""),
        (',', "Bottom/Back", ""),
        (';', "Ignore", "")]
    surf_class_orient = EnumProperty(
        items=surf_class_orient_enum, name="Orientation",
        description="Volume molecules affected at front or back of a surface. "
                    "Surface molecules affected by orientation at border.",
        update=cellblender_operators.check_surf_class_props)
    surf_class_type_enum = [
        ('ABSORPTIVE', "Absorptive", ""),
        ('TRANSPARENT', "Transparent", ""),
        ('REFLECTIVE', "Reflective", ""),
        ('CLAMP_CONCENTRATION', "Clamp Concentration", "")]
    surf_class_type = EnumProperty(
        items=surf_class_type_enum, name="Type",
        description="Molecules are destroyed by absorptive surfaces, pass "
                    "through transparent, and \"bounce\" off of reflective.",
        update=cellblender_operators.check_surf_class_props)
    clamp_value = FloatProperty(name="Value", precision=4, min=0.0)
    clamp_value_str = StringProperty(
        name="Value", description="Concentration Units: Molar",
        update=cellblender_operators.update_clamp_value)
    status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        sc = self
        sc_dict = {}
        sc_dict['name'] = sc.name
        sc_dict['molecule'] = sc.molecule
        sc_dict['surf_class_orient'] = str(sc.surf_class_orient)
        sc_dict['surf_class_type'] = str(sc.surf_class_type)
        sc_dict['clamp_value'] = str(sc.clamp_value_str)
        return sc_dict



class MCellSurfaceClassesProperty(bpy.types.PropertyGroup):
    """ Stores the surface class name and a list of its properties. """

    name = StringProperty(
        name="Surface Class Name", default="Surface_Class",
        description="This name can be selected in Modify Surface Regions.",
        update=cellblender_operators.check_surface_class)
    surf_class_props_list = CollectionProperty(
        type=MCellSurfaceClassPropertiesProperty, name="Surface Classes List")
    active_surf_class_props_index = IntProperty(
        name="Active Surface Class Index", default=0)
    status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        print ( "Surface Classes building Data Model" )
        sc_dm = {}
        sc_dm['name'] = self.name
        sc_list = []
        for sc in self.surf_class_props_list:
            sc_list.append ( sc.build_data_model_from_properties(context) )
        sc_dm['surface_class_prop_list'] = sc_list
        return sc_dm


class MCellModSurfRegionsProperty(bpy.types.PropertyGroup):
    """ Assign a surface class to a surface region. """

    name = StringProperty(name="Modify Surface Region")
    surf_class_name = StringProperty(
        name="Surface Class Name",
        description="This surface class will be assigned to the surface "
                    "region listed below.",
        update=cellblender_operators.check_mod_surf_regions)
    object_name = StringProperty(
        name="Object Name",
        description="A region on this object will have the above surface "
                    "class assigned to it.",
        update=cellblender_operators.check_mod_surf_regions)
    region_name = StringProperty(
        name="Region Name",
        description="This surface region will have the above surface class "
                    "assigned to it.",
        update=cellblender_operators.check_mod_surf_regions)
    status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        print ( "Surface Region building Data Model" )
        sr_dm = {}
        sr_dm['name'] = self.name
        sr_dm['surf_class_name'] = self.surf_class_name
        sr_dm['object_name'] = self.object_name
        sr_dm['region_name'] = self.region_name
        return sr_dm



#Panel Properties:

class CellBlenderPreferencesPanelProperty(bpy.types.PropertyGroup):

    mcell_binary = StringProperty(name="MCell Binary",
        update=cellblender_operators.check_mcell_binary)
    mcell_binary_valid = BoolProperty(name="MCell Binary Valid",
        default=False)
    python_binary = StringProperty(name="Python Binary",
        update=cellblender_operators.check_python_binary)
    python_binary_valid = BoolProperty(name="Python Binary Valid",
        default=False)
    bionetgen_location = StringProperty(name="BioNetGen Location",
        update=cellblender_operators.check_bionetgen_location)
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
        update=cellblender_operators.save_preferences)
    decouple_export_run = BoolProperty(
        name="Decouple Export and Run", default=False,
        description="Allow the project to be exported without also running"
                    " the simulation.",
        update=cellblender_operators.save_preferences)
    debug_level = IntProperty(
        name="Debug", default=0, min=0, max=100,
        description="Amount of debug information to print: 0 to 100")


class MCellScratchPanelProperty(bpy.types.PropertyGroup):
    show_all_icons = BoolProperty(
        name="Show All Icons",
        description="Show all Blender icons and their names",
        default=False)
    print_all_icons = BoolProperty(
        name="Print All Icon Names",
        description="Print all Blender icon names (helpful for searching)",
        default=False)


class MCellProjectPanelProperty(bpy.types.PropertyGroup):
    base_name = StringProperty(
        name="Project Base Name", default="cellblender_project")

    status = StringProperty(name="Status")


class MCellExportProjectPanelProperty(bpy.types.PropertyGroup):
    export_format_enum = [
        ('mcell_mdl_unified', "Single Unified MCell MDL File", ""),
        ('mcell_mdl_modular', "Modular MCell MDL Files", "")]
    export_format = EnumProperty(items=export_format_enum,
                                 name="Export Format",
                                 default='mcell_mdl_modular')


class MCellRunSimulationProcessesProperty(bpy.types.PropertyGroup):
    name = StringProperty(name="Simulation Runner Process")
    #pid = IntProperty(name="PID")


class MCellRunSimulationPanelProperty(bpy.types.PropertyGroup):
    start_seed = IntProperty(
        name="Start Seed", default=1, min=1,
        description="The starting value of the random number generator seed")
    end_seed = IntProperty(
        name="End Seed", default=1, min=1,
        description="The ending value of the random number generator seed")
    mcell_processes = IntProperty(
        name="Number of Processes",
        default=cpu_count(),
        min=1,
        max=cpu_count(),
        description="Number of simultaneous MCell processes")
    log_file_enum = [
        ('none', "Do not Generate", ""),
        ('file', "Send to File", ""),
        ('console', "Send to Console", "")]
    log_file = EnumProperty(
        items=log_file_enum, name="Output Log", default='console',
        description="Where to send MCell log output")
    error_file_enum = [
        ('none', "Do not Generate", ""),
        ('file', "Send to File", ""),
        ('console', "Send to Console", "")]
    error_file = EnumProperty(
        items=error_file_enum, name="Error Log", default='console',
        description="Where to send MCell error output")
    remove_append_enum = [
        ('remove', "Remove Previous Data", ""),
        ('append', "Append to Previous Data", "")]
    remove_append = EnumProperty(
        items=remove_append_enum, name="Previous Simulation Data",
        default='remove',
        description="Remove or append to existing rxn/viz data from previous"
                    " simulations before running new simulations.")
    processes_list = CollectionProperty(
        type=MCellRunSimulationProcessesProperty,
        name="Simulation Runner Processes")
    active_process_index = IntProperty(
        name="Active Simulation Runner Process Index", default=0)
    status = StringProperty(name="Status")
    error_list = CollectionProperty(
        type=MCellStringProperty,
        name="Error List")
    active_err_index = IntProperty(
        name="Active Error Index", default=0)


class MCellMolVizPanelProperty(bpy.types.PropertyGroup):
    """ Property group for for molecule visualization.

    This is the "Visualize Simulation Results Panel".

    """

    mol_viz_seed_list = CollectionProperty(
        type=MCellStringProperty, name="Visualization Seed List")
    active_mol_viz_seed_index = IntProperty(
        name="Current Visualization Seed Index", default=0,
        update=cellblender_operators.read_viz_data)
        #update= bpy.ops.mcell.read_viz_data)
    mol_file_dir = StringProperty(
        name="Molecule File Dir", subtype='NONE')
    mol_file_list = CollectionProperty(
        type=MCellStringProperty, name="Molecule File Name List")
    mol_file_num = IntProperty(
        name="Number of Molecule Files", default=0)
    mol_file_name = StringProperty(
        name="Current Molecule File Name", subtype='NONE')
    mol_file_index = IntProperty(name="Current Molecule File Index", default=0)
    mol_file_start_index = IntProperty(
        name="Molecule File Start Index", default=0)
    mol_file_stop_index = IntProperty(
        name="Molecule File Stop Index", default=0)
    mol_file_step_index = IntProperty(
        name="Molecule File Step Index", default=1)
    mol_viz_list = CollectionProperty(
        type=MCellStringProperty, name="Molecule Viz Name List")
    render_and_save = BoolProperty(name="Render & Save Images")
    mol_viz_enable = BoolProperty(
        name="Enable Molecule Vizualization",
        description="Disable for faster animation preview",
        default=True, update=cellblender_operators.mol_viz_update)
    color_list = CollectionProperty(
        type=MCellFloatVectorProperty, name="Molecule Color List")
    color_index = IntProperty(name="Color Index", default=0)
    manual_select_viz_dir = BoolProperty(
        name="Manually Select Viz Directory", default=False,
        description="Toggle the option to manually load viz data.",
        update=cellblender_operators.mol_viz_toggle_manual_select)


from . import parameter_system


class MCellInitializationPanelProperty(bpy.types.PropertyGroup):

    def __init__(self):
        print ( "\n\nMCellInitializationPanelProperty.__init__() called\n\n" )

    iterations = PointerProperty ( name="iterations", type=parameter_system.Parameter_Reference )
    time_step =  PointerProperty ( name="Time Step", type=parameter_system.Parameter_Reference )

    status = StringProperty(name="Status")
    advanced = bpy.props.BoolProperty(default=False)
    warnings = bpy.props.BoolProperty(default=False)
    notifications = bpy.props.BoolProperty(default=False)

    # Advanced/Optional Commands

    time_step_max = PointerProperty ( name="Time Step Max", type=parameter_system.Parameter_Reference )
    space_step = PointerProperty ( name="Space Step", type=parameter_system.Parameter_Reference )
    interaction_radius = PointerProperty ( name="Interaction Radius", type=parameter_system.Parameter_Reference )
    radial_directions = PointerProperty ( name="Radial Directions", type=parameter_system.Parameter_Reference )
    radial_subdivisions = PointerProperty ( name="Radial Subdivisions", type=parameter_system.Parameter_Reference )
    vacancy_search_distance = PointerProperty ( name="Radial Subdivisions", type=parameter_system.Parameter_Reference )
    surface_grid_density = PointerProperty ( name="Surface Grid Density", type=parameter_system.Parameter_Reference )

    def init_properties ( self, parameter_system ):
        self.iterations.init_ref    ( parameter_system, "Iteration_Type", 
                                      user_name="Iterations", 
                                      user_expr="1",    
                                      user_units="",  
                                      user_descr="Number of iterations to run",  
                                      user_int=True )
        self.time_step.init_ref     ( parameter_system, "Time_Step_Type", 
                                      user_name="Time Step",  
                                      user_expr="1e-6", 
                                      user_units="seconds", 
                                      user_descr="Simulation Time Step" )
        self.time_step_max.init_ref ( parameter_system, "Time_Step_Max_Type", 
                                      user_name="Maximum Time Step", 
                                      user_expr="", 
                                      user_units="seconds", 
                                      user_descr="The longest possible time step" )
        self.space_step.init_ref    ( parameter_system, "Space_Step_Type",    
                                      user_name="Space Step",    
                                      user_expr="", 
                                      user_units="microns", 
                                      user_descr="Have molecules take the same mean diffusion distance" )
        self.interaction_radius.init_ref ( parameter_system, "Int_Rad_Type", 
                                           user_name="Interaction Radius", 
                                           user_expr="", user_units="microns", 
                                           user_descr="Molecules will interact when they get within N microns" )
        self.radial_directions.init_ref   ( parameter_system, "Rad_Dir_Type", 
                                            user_name="Radial Directions",   
                                            user_expr="", user_units="microns", 
                                            user_descr="Number of different directions to put in lookup table\nLeave alone unless you know what you are doing" )
        self.radial_subdivisions.init_ref ( parameter_system, "Rad_Sub_Type", 
                                            user_name="Radial Subdivisions", 
                                            user_expr="", 
                                            user_units="microns", 
                                            user_descr="Molecules will interact when they get within N microns" )
        self.vacancy_search_distance.init_ref ( parameter_system, "Vac_SD_Type", 
                                                user_name="Vacancy Search Distance", 
                                                user_expr="", 
                                                user_units="microns", 
                                                user_descr="Surface molecule products can be created at N distance" )
        self.surface_grid_density.init_ref ( parameter_system, "Int_Rad_Type", 
                                             user_name="Surface Grid Density", 
                                             user_expr="10000", 
                                             user_units="count / sq micron", 
                                             user_descr="Number of molecules that can be stored per square micron" )

    def build_data_model_from_properties ( self, context ):
        dm_dict = {}

        dm_dict['iterations'] = self.iterations.get_expr()
        dm_dict['time_step'] = self.time_step.get_expr()
        dm_dict['time_step_max'] = self.time_step_max.get_expr()
        dm_dict['space_step'] = self.space_step.get_expr()
        dm_dict['interaction_radius'] = self.interaction_radius.get_expr()
        dm_dict['radial_directions'] = self.radial_directions.get_expr()
        dm_dict['radial_subdivisions'] = self.radial_subdivisions.get_expr()
        dm_dict['vacancy_search_distance'] = self.vacancy_search_distance.get_expr()
        dm_dict['surface_grid_density'] = self.surface_grid_density.get_expr()
        dm_dict['microscopic_reversibility'] = str(self.microscopic_reversibility)
        dm_dict['accurate_3d_reactions'] = self.accurate_3d_reactions==True
        dm_dict['center_molecules_on_grid'] = self.center_molecules_grid==True

        notify_dict = {}
        notify_dict['all_notifications'] = str(self.all_notifications)
        notify_dict['diffusion_constant_report'] = str(self.diffusion_constant_report)
        notify_dict['file_output_report'] = self.file_output_report==True
        notify_dict['final_summary'] = self.final_summary==True
        notify_dict['iteration_report'] = self.iteration_report==True
        notify_dict['partition_location_report'] = self.partition_location_report==True
        notify_dict['probability_report'] = str(self.probability_report)
        notify_dict['probability_report_threshold'] = str(self.probability_report_threshold)
        notify_dict['varying_probability_report'] = self.varying_probability_report==True
        notify_dict['progress_report'] = self.progress_report==True
        notify_dict['release_event_report'] = self.release_event_report==True
        notify_dict['molecule_collision_report'] = self.molecule_collision_report==True
        notify_dict['box_triangulation_report'] = False
        dm_dict['notifications'] = notify_dict
        
        warn_dict = {}
        warn_dict['all_warnings'] = str(self.all_warnings)
        warn_dict['degenerate_polygons'] = str(self.degenerate_polygons)
        warn_dict['high_reaction_probability'] = str(self.high_reaction_probability)
        warn_dict['high_probability_threshold'] = str(self.high_probability_threshold)
        warn_dict['lifetime_too_short'] = str(self.lifetime_too_short)
        warn_dict['lifetime_threshold'] = str(self.lifetime_threshold)
        warn_dict['missed_reactions'] = str(self.missed_reactions)
        warn_dict['missed_reaction_threshold'] = str(self.missed_reaction_threshold)
        warn_dict['negative_diffusion_constant'] = str(self.negative_diffusion_constant)
        warn_dict['missing_surface_orientation'] = str(self.missing_surface_orientation)
        warn_dict['negative_reaction_rate'] = str(self.negative_reaction_rate)
        warn_dict['useless_volume_orientation'] = str(self.useless_volume_orientation)
        dm_dict['warnings'] = warn_dict

        return dm_dict


    accurate_3d_reactions = BoolProperty(
        name="Accurate 3D Reaction",
        description="If selected, molecules will look through partitions to "
                    "react.",
        default=True)
    center_molecules_grid = BoolProperty(
        name="Center Molecules on Grid",
        description="If selected, surface molecules will be centered on the "
                    "grid.",
        default=False)


    microscopic_reversibility_enum = [
        ('ON', "On", ""),
        ('OFF', "Off", ""),
        ('SURFACE_ONLY', "Surface Only", ""),
        ('VOLUME_ONLY', "Volume Only", "")]
    microscopic_reversibility = EnumProperty(
        items=microscopic_reversibility_enum, name="Microscopic Reversibility",
        description="If false, more efficient but less accurate reactions",
        default='OFF')

    # Notifications
    all_notifications_enum = [
        ('INDIVIDUAL', "Set Individually", ""),
        ('ON', "On", ""),
        ('OFF', "Off", "")]
    all_notifications = EnumProperty(
        items=all_notifications_enum, name="All Notifications",
        description="If on/off, all notifications will be set to on/off "
                    "respectively.",
        default='INDIVIDUAL')
    diffusion_constant_report_enum = [
        ('BRIEF', "Brief", ""),
        ('ON', "On", ""),
        ('OFF', "Off", "")]
    diffusion_constant_report = EnumProperty(
        items=diffusion_constant_report_enum, name="Diffusion Constant Report",
        description="If brief, Mcell will report average diffusion distance "
                    "per step for each molecule.")
    file_output_report = BoolProperty(
        name="File Output Report",
        description="If selected, MCell will report every time that reaction "
                    "data is written.",
        default=False)
    final_summary = BoolProperty(
        name="Final Summary",
        description="If selected, MCell will report about the CPU time used",
        default=True)
    iteration_report = BoolProperty(
        name="Iteration Report",
        description="If selected, MCell will report how many iterations have "
                    "completed based on total.",
        default=True)
    partition_location_report = BoolProperty(
        name="Partition Location Report",
        description="If selected, the partition locations will be printed.",
        default=False)
    probability_report_enum = [
        ('ON', "On", ""),
        ('OFF', "Off", ""),
        ('THRESHOLD', "Threshold", "")]
    probability_report = EnumProperty(
        items=probability_report_enum, name="Probability Report", default='ON',
        description="If on, MCell will report reaction probabilites for each "
                    "reaction.")
    probability_report_threshold = bpy.props.FloatProperty(
        name="Threshold", min=0.0, max=1.0, precision=2)
    varying_probability_report = BoolProperty(
        name="Varying Probability Report",
        description="If selected, MCell will print out the reaction "
                    "probabilites for time-varying reaction.",
        default=True)
    progress_report = BoolProperty(
        name="Progress Report",
        description="If selected, MCell will print out messages indicating "
                    "which part of the simulation is underway.",
        default=True)
    release_event_report = BoolProperty(
        name="Release Event Report",
        description="If selected, MCell will print a message every time "
                    "molecules are released through a release site.",
        default=True)
    molecule_collision_report = BoolProperty(
        name="Molecule Collision Report",
        description="If selected, MCell will print the number of "
                    "bi/trimolecular collisions that occured.",
        default=False)

    # Warnings
    all_warnings_enum = [
        ('INDIVIDUAL', "Set Individually", ""),
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    all_warnings = EnumProperty(
        items=all_warnings_enum, name="All Warnings",
        description="If not \"Set Individually\", all warnings will be set "
                    "the same.",
        default='INDIVIDUAL')
    degenerate_polygons_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    degenerate_polygons = EnumProperty(
        items=degenerate_polygons_enum, name="Degenerate Polygons",
        description="Degenerate polygons have zero area and must be removed.",
        default='WARNING')
    high_reaction_probability_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    high_reaction_probability = EnumProperty(
        items=high_reaction_probability_enum, name="High Reaction Probability",
        description="Generate warnings or errors if probability reaches a "
                    "specified threshold.",
        default='IGNORED')
    high_probability_threshold = bpy.props.FloatProperty(
        name="High Probability Threshold", min=0.0, max=1.0, default=1.0,
        precision=2)
    lifetime_too_short_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", "")]
    lifetime_too_short = EnumProperty(
        items=lifetime_too_short_enum, name="Lifetime Too Short",
        description="Generate warning if molecules have short lifetimes.",
        default='WARNING')
    lifetime_threshold = IntProperty(
        name="Threshold", min=0, default=50)
    missed_reactions_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", "")]
    missed_reactions = EnumProperty(
        items=missed_reactions_enum, name="Missed Reactions",
        description="Generate warning if there are missed reactions.",
        default='WARNING')
    missed_reaction_threshold = bpy.props.FloatProperty(
        name="Threshold", min=0.0, max=1.0, default=0.001,
        precision=4)
    negative_diffusion_constant_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    negative_diffusion_constant = EnumProperty(
        items=negative_diffusion_constant_enum,
        description="Diffusion constants cannot be negative and will be set "
                    "to zero.",
        name="Negative Diffusion Constant", default='WARNING')
    missing_surface_orientation_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    missing_surface_orientation = EnumProperty(
        items=missing_surface_orientation_enum,
        description="Generate errors/warnings if molecules are placed on "
                    "surfaces or reactions occur at surfaces without "
                    "specified orientation.",
        name="Missing Surface Orientation",
        default='ERROR')
    negative_reaction_rate_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    negative_reaction_rate = EnumProperty(
        items=negative_reaction_rate_enum, name="Negative Reaction Rate",
        description="Reaction rates cannot be negative and will be set "
                    "to zero.",
        default='WARNING')
    useless_volume_orientation_enum = [
        ('IGNORED', "Ignored", ""),
        ('WARNING', "Warning", ""),
        ('ERROR', "Error", "")]
    useless_volume_orientation = EnumProperty(
        items=useless_volume_orientation_enum,
        description="Generate errors/warnings if molecules are released in a "
                    "volume or reactions occur in a volume with specified "
                    "orientation.",
        name="Useless Volume Orientation", default='WARNING')


class MCellPartitionsPanelProperty(bpy.types.PropertyGroup):
    include = BoolProperty(
        name="Include Partitions",
        description="Partitions are a way of speeding up a simulation if used "
                    "properly.",
        default=False)
    recursion_flag = BoolProperty(
        name="Recursion Flag",
        description="Flag to prevent infinite recursion",
        default=False)
    x_start = bpy.props.FloatProperty(
        name="X Start", default=-1, precision=3,
        description="The start of the partitions on the x-axis",
        update=cellblender_operators.transform_x_partition_boundary)
    x_end = bpy.props.FloatProperty(
        name="X End", default=1, precision=3,
        description="The end of the partitions on the x-axis",
        update=cellblender_operators.transform_x_partition_boundary)
    x_step = bpy.props.FloatProperty(
        name="X Step", default=0.02, precision=3,
        description="The distance between partitions on the x-axis",
        update=cellblender_operators.check_x_partition_step)
    y_start = bpy.props.FloatProperty(
        name="Y Start", default=-1, precision=3,
        description="The start of the partitions on the y-axis",
        update=cellblender_operators.transform_y_partition_boundary)
    y_end = bpy.props.FloatProperty(
        name="Y End", default=1, precision=3,
        description="The end of the partitions on the y-axis",
        update=cellblender_operators.transform_y_partition_boundary)
    y_step = bpy.props.FloatProperty(
        name="Y Step", default=0.02, precision=3,
        description="The distance between partitions on the y-axis",
        update=cellblender_operators.check_y_partition_step)
    z_start = bpy.props.FloatProperty(
        name="Z Start", default=-1, precision=3,
        description="The start of the partitions on the z-axis",
        update=cellblender_operators.transform_z_partition_boundary)
    z_end = bpy.props.FloatProperty(
        name="Z End", default=1, precision=3,
        description="The end of the partitions on the z-axis",
        update=cellblender_operators.transform_z_partition_boundary)
    z_step = bpy.props.FloatProperty(
        name="Z Step", default=0.02, precision=3,
        description="The distance between partitions on the z-axis",
        update=cellblender_operators.check_z_partition_step)

    def build_data_model_from_properties ( self, context ):
        print ( "Partitions building Data Model" )
        dm_dict = {}
        dm_dict['include'] = self.include==True
        dm_dict['recursion_flag'] = self.recursion_flag==True
        dm_dict['x_start'] = str(self.x_start)
        dm_dict['x_end'] =   str(self.x_end)
        dm_dict['x_step'] =  str(self.x_step)
        dm_dict['y_start'] = str(self.y_start)
        dm_dict['y_end'] =   str(self.y_end)
        dm_dict['y_step'] =  str(self.y_step)
        dm_dict['x_start'] = str(self.z_start)
        dm_dict['z_end'] =   str(self.z_end)
        dm_dict['z_step'] =  str(self.z_step)
        return dm_dict



####################### DB: added for imported parameters from BNG, SBML or other models###############################
class MCellParameterProperty(bpy.types.PropertyGroup):
    name = StringProperty(name="Parameter Name", default="Parameter")
    value = StringProperty(name="Parameter Value", default="0")
    unit = StringProperty(name="Parameter Unit", default="",
        description="Forward Rate Units: sec^-1 (unimolecular),"
                    " M^-1*sec^-1 (bimolecular)")
    type = StringProperty(name="Parameter type", default="", description="")		    
    status = StringProperty(name="Status")

class MCellParametersPanelProperty(bpy.types.PropertyGroup):
    parameter_list = CollectionProperty(
        type=MCellParameterProperty, name="Parameter List")
    active_par_index = IntProperty(name="Active Parameter Index", default=0)
    plot_command = StringProperty(name="", default="")
##########################################################################################################################


class MCellReactionsPanelProperty(bpy.types.PropertyGroup):
    reaction_list = CollectionProperty(
        type=MCellReactionProperty, name="Reaction List")
    active_rxn_index = IntProperty(name="Active Reaction Index", default=0)
    reaction_name_list = CollectionProperty(
        type=MCellStringProperty, name="Reaction Name List")
    plot_command = StringProperty(name="", default="")

    def build_data_model_from_properties ( self, context ):
        print ( "Reaction List building Data Model" )
        react_dm = {}
        react_list = []
        for r in self.reaction_list:
            react_list.append ( r.build_data_model_from_properties(context) )
        react_dm['reaction_list'] = react_list
        return react_dm


class MCellSurfaceClassesPanelProperty(bpy.types.PropertyGroup):
    surf_class_list = CollectionProperty(
        type=MCellSurfaceClassesProperty, name="Surface Classes List")
    active_surf_class_index = IntProperty(
        name="Active Surface Class Index", default=0)
    #surf_class_props_status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        print ( "Surface Classes Panel building Data Model" )
        sc_dm = {}
        sc_list = []
        for sc in self.surf_class_list:
            sc_list.append ( sc.build_data_model_from_properties(context) )
        sc_dm['surface_class_list'] = sc_list
        return sc_dm


class MCellModSurfRegionsPanelProperty(bpy.types.PropertyGroup):
    mod_surf_regions_list = CollectionProperty(
        type=MCellModSurfRegionsProperty, name="Modify Surface Region List")
    active_mod_surf_regions_index = IntProperty(
        name="Active Modify Surface Region Index", default=0)

    def build_data_model_from_properties ( self, context ):
        print ( "Assign Surface Class List building Data Model" )
        sr_dm = {}
        sr_list = []
        for sr in self.mod_surf_regions_list:
            sr_list.append ( sr.build_data_model_from_properties(context) )
        sr_dm['modify_surface_regions_list'] = sr_list
        return sr_dm



class MCellReleasePatternPanelProperty(bpy.types.PropertyGroup):
    release_pattern_list = CollectionProperty(
        type=MCellReleasePatternProperty, name="Release Pattern List")
    release_pattern_rxn_name_list = CollectionProperty(
        type=MCellStringProperty,
        name="Release Pattern and Reaction Name List")
    active_release_pattern_index = IntProperty(
        name="Active Release Pattern Index", default=0)

    def build_data_model_from_properties ( self, context ):
        print ( "Release Pattern List building Data Model" )
        rel_pat_dm = {}
        rel_pat_list = []
        for r in self.release_pattern_list:
            rel_pat_list.append ( r.build_data_model_from_properties(context) )
        rel_pat_dm['release_pattern_list'] = rel_pat_list
        return rel_pat_dm


class MCellMoleculeReleasePanelProperty(bpy.types.PropertyGroup):
    mol_release_list = CollectionProperty(
        type=MCellMoleculeReleaseProperty, name="Molecule Release List")
    active_release_index = IntProperty(name="Active Release Index", default=0)

    def build_data_model_from_properties ( self, context ):
        print ( "Release Site List building Data Model" )
        rel_site_dm = {}
        rel_site_list = []
        for r in self.mol_release_list:
            rel_site_list.append ( r.build_data_model_from_properties(context) )
        rel_site_dm['release_site_list'] = rel_site_list
        return rel_site_dm



class MCellModelObjectsProperty(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Object Name", update=cellblender_operators.check_model_object)
    status = StringProperty(name="Status")


class MCellModelObjectsPanelProperty(bpy.types.PropertyGroup):
    object_list = CollectionProperty(
        type=MCellModelObjectsProperty, name="Object List")
    active_obj_index = IntProperty(name="Active Object Index", default=0)

    def build_data_model_from_properties ( self, context ):
    
        print ( "Model Objects List building Data Model" )
        mo_dm = {}
        mo_list = []
        for scene_object in context.scene.objects:
            if scene_object.type == 'MESH':
                if scene_object.mcell.include:
                    print ( "MCell object: " + scene_object.name )
                    mo_list.append ( { "name": scene_object.name } )
        mo_dm['model_object_list'] = mo_list
        return mo_dm


    def build_data_model_materials_from_materials ( self, context ):
        print ( "Model Objects List building Materials for Data Model" )
        mat_dm = {}
        mat_dict = {}

        # First build the list of materials from all objects
        for data_object in context.scene.objects:
            if data_object.type == 'MESH':
                if data_object.mcell.include:
                    print ( "Saving Materials for: " + data_object.name )
                    for mat_slot in data_object.material_slots:
                        if not mat_slot.name in mat_dict:
                            # This is a new material, so add it
                            mat = bpy.data.materials[mat_slot.name]
                            print ( "  Adding " + mat_slot.name )
                            mat_obj = {}
                            mat_obj['diffuse_color'] = {
                                'r': mat.diffuse_color.r,
                                'g': mat.diffuse_color.g,
                                'b': mat.diffuse_color.b,
                                'a': mat.alpha }
                            # Need to set:
                            #  mat.use_transparency
                            #  obj.show_transparent
                            mat_dict[mat_slot.name] = mat_obj;
        mat_dm['material_dict'] = mat_dict
        return mat_dm


    def build_data_model_geometry_from_mesh ( self, context ):
        print ( "Model Objects List building Geometry for Data Model" )
        g_dm = {}
        g_list = []

        for data_object in context.scene.objects:
            if data_object.type == 'MESH':
                if data_object.mcell.include:
                    print ( "MCell object: " + data_object.name )

                    g_obj = {}
                    
                    saved_hide_status = data_object.hide
                    data_object.hide = False

                    context.scene.objects.active = data_object
                    bpy.ops.object.mode_set(mode='OBJECT')

                    g_obj['name'] = data_object.name
                    
                    loc_x = data_object.location.x
                    loc_y = data_object.location.y
                    loc_z = data_object.location.z

                    g_obj['location'] = [loc_x, loc_y, loc_z]
                    
                    if len(data_object.data.materials) > 0:
                        g_obj['material_names'] = []
                        for mat in data_object.data.materials:
                            g_obj['material_names'].append ( mat.name )
                            # g_obj['material_name'] = data_object.data.materials[0].name
                    
                    v_list = []
                    mesh = data_object.data
                    matrix = data_object.matrix_world
                    vertices = mesh.vertices
                    for v in vertices:
                        t_vec = matrix * v.co
                        v_list.append ( [t_vec.x-loc_x, t_vec.y-loc_y, t_vec.z-loc_z] )
                    g_obj['vertex_list'] = v_list

                    f_list = []
                    faces = mesh.polygons
                    for f in faces:
                        f_list.append ( [f.vertices[0], f.vertices[1], f.vertices[2]] )
                    g_obj['element_connections'] = f_list
                    
                    if len(data_object.data.materials) > 1:
                        # This object has multiple materials, so store the material index for each face
                        mi_list = []
                        for f in faces:
                            mi_list.append ( f.material_index )
                        g_obj['element_material_indices'] = mi_list

                    regions = data_object.mcell.get_regions_dictionary(data_object)
                    if regions:
                        r_list = []

                        region_names = [k for k in regions.keys()]
                        region_names.sort()
                        for region_name in region_names:
                            rgn = {}
                            rgn['name'] = region_name
                            rgn['include_elements'] = regions[region_name]
                            r_list.append ( rgn )
                        g_obj['define_surface_regions'] = r_list

                    # restore proper object visibility state
                    data_object.hide = saved_hide_status

                    g_list.append ( g_obj )

        g_dm['object_list'] = g_list
        return g_dm




class MCellVizOutputPanelProperty(bpy.types.PropertyGroup):
    active_mol_viz_index = IntProperty(
        name="Active Molecule Viz Index", default=0)
    all_iterations = bpy.props.BoolProperty(
        name="All Iterations",
        description="Include all iterations for visualization.", default=True)
    start = bpy.props.IntProperty(
        name="Start", description="Starting iteration", default=0, min=0)
    end = bpy.props.IntProperty(
        name="End", description="Ending iteration", default=1, min=1)
    step = bpy.props.IntProperty(
        name="Step", description="Output viz data every n iterations.",
        default=1, min=1)
    export_all = BoolProperty(
        name="Export All",
        description="Visualize all molecules",
        default=False)

    def build_data_model_from_properties ( self, context ):
        print ( "Viz Output building Data Model" )
        vo_dm = {}
        vo_dm['all_iterations'] = self.all_iterations
        vo_dm['start'] = str(self.start)
        vo_dm['end'] = str(self.end)
        vo_dm['step'] = str(self.step)
        vo_dm['export_all'] = self.export_all
        return vo_dm


class MCellReactionOutputProperty(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Reaction Output", update=cellblender_operators.check_rxn_output)
    molecule_name = StringProperty(
        name="Molecule",
        description="Count the selected molecule.",
        update=cellblender_operators.check_rxn_output)
    reaction_name = StringProperty(
        name="Reaction",
        description="Count the selected reaction.",
        update=cellblender_operators.check_rxn_output)
    object_name = StringProperty(
        name="Object", update=cellblender_operators.check_rxn_output)
    region_name = StringProperty(
        name="Region", update=cellblender_operators.check_rxn_output)
    count_location_enum = [
        ('World', "World", ""),
        ('Object', "Object", ""),
        ('Region', "Region", "")]
    count_location = bpy.props.EnumProperty(
        items=count_location_enum, name="Count Location",
        description="Count all molecules in the selected location.",
        update=cellblender_operators.check_rxn_output)
    rxn_or_mol_enum = [
        ('Reaction', "Reaction", ""),
        ('Molecule', "Molecule", "")]
    rxn_or_mol = bpy.props.EnumProperty(
        items=rxn_or_mol_enum, name="Count Reaction or Molecule",
        default='Molecule',
        description="Select between counting a reaction or molecule.",
        update=cellblender_operators.check_rxn_output)
    plot_command = StringProperty(
        name="Command")  # , update=cellblender_operators.check_rxn_output)
    status = StringProperty(name="Status")

    def build_data_model_from_properties ( self, context ):
        print ( "Reaction Output building Data Model" )
        ro_dm = {}
        ro_dm['name'] = self.name
        ro_dm['molecule_name'] = self.molecule_name
        ro_dm['reaction_name'] = self.reaction_name
        ro_dm['object_name'] = self.object_name
        ro_dm['region_name'] = self.region_name
        ro_dm['count_location'] = self.count_location
        ro_dm['rxn_or_mol'] = self.rxn_or_mol
        return ro_dm



import cellblender

#JJT:temporary class
class MCellReactionOutputPropertyTemp(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Reaction Output")
    molecule_name = StringProperty(
        name="Molecule",
        description="Count the selected molecules.")


class MCellReactionOutputPanelProperty(bpy.types.PropertyGroup):
    #JJT: temporary list made to hold complex expressions from imported files
    temp_index = IntProperty(
        name="Temp Output Index", default=0)
    complex_rxn_output_list = CollectionProperty(
        type=MCellReactionOutputPropertyTemp,name="Temporary output list")
    
    active_rxn_output_index = IntProperty(
        name="Active Reaction Output Index", default=0)
    rxn_output_list = CollectionProperty(
        type=MCellReactionOutputProperty, name="Reaction Output List")
    plot_layout_enum = [
        (' page ', "Separate Page for each Plot", ""),
        (' plot ', "One Page, Multiple Plots", ""),
        (' ',      "One Page, One Plot", "")]
    plot_layout = bpy.props.EnumProperty ( items=plot_layout_enum, name="" )
    plot_legend_enum = [
        ('x', "No Legend", ""),
        ('0', "Legend with Automatic Placement", ""),
        ('1', "Legend in Upper Right", ""),
        ('2', "Legend in Upper Left", ""),
        ('3', "Legend in Lower Left", ""),
        ('4', "Legend in Lower Right", ""),
        # ('5', "Legend on Right", ""), This appears to duplicate option 7
        ('6', "Legend in Center Left", ""),
        ('7', "Legend in Center Right", ""),
        ('8', "Legend in Lower Center", ""),
        ('9', "Legend in Upper Center", ""),
        ('10', "Legend in Center", "")]
    plot_legend = bpy.props.EnumProperty ( items=plot_legend_enum, name="", default='0' )
    combine_seeds = BoolProperty(
        name="Combine Seeds",
        description="Combine all seeds onto the same plot.",
        default=True)
    mol_colors = BoolProperty(
        name="Molecule Colors",
        description="Use Molecule Colors for line colors.",
        default=False)

    def build_data_model_from_properties ( self, context ):
        print ( "Reaction Output Panel building Data Model" )
        ro_dm = {}
        ro_dm['plot_layout'] = self.plot_layout
        ro_dm['plot_legend'] = self.plot_legend
        ro_dm['combine_seeds'] = self.combine_seeds
        ro_dm['mol_colors'] = self.mol_colors
        ro_list = []
        for ro in self.rxn_output_list:
            ro_list.append ( ro.build_data_model_from_properties(context) )
        ro_dm['reaction_output_list'] = ro_list
        return ro_dm


class MCellMoleculeGlyphsPanelProperty(bpy.types.PropertyGroup):
    glyph_lib = __file__.replace(__file__.split('/')[len(
        __file__.split("/"))-1], "")+"glyph_library.blend/Mesh/"
    glyph_enum = [
        ('Cone', "Cone", ""),
        ('Cube', "Cube", ""),
        ('Cylinder', "Cylinder", ""),
        ('Icosahedron', "Icosahedron", ""),
        ('Octahedron', "Octahedron", ""),
        ('Receptor', "Receptor", ""),
        ('Sphere_1', "Sphere_1", ""),
        ('Sphere_2', "Sphere_2", ""),
        ('Torus', "Torus", "")]
    glyph = EnumProperty(items=glyph_enum, name="Molecule Shapes")
    status = StringProperty(name="Status")


class MCellMeshalyzerPanelProperty(bpy.types.PropertyGroup):
    object_name = StringProperty(name="Object Name")
    vertices = IntProperty(name="Vertices", default=0)
    edges = IntProperty(name="Edges", default=0)
    faces = IntProperty(name="Faces", default=0)
    watertight = StringProperty(name="Watertight")
    manifold = StringProperty(name="Manifold")
    normal_status = StringProperty(name="Surface Normals")
    area = FloatProperty(name="Area", default=0)
    volume = FloatProperty(name="Volume", default=0)
    sav_ratio = FloatProperty(name="SA/V Ratio", default=0)
    status = StringProperty(name="Status")


class MCellObjectSelectorPanelProperty(bpy.types.PropertyGroup):
    filter = StringProperty(
        name="Object Name Filter",
        description="Enter a regular expression for object names.")




class PP_OT_init_mcell(bpy.types.Operator):
    bl_idname = "mcell.init_cellblender"
    bl_label = "Init CellBlender"
    bl_description = "Initialize CellBlender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print ( "Initializing CellBlender" )
        context.scene.mcell.init_properties()
        print ( "CellBlender has been initialized" )
        return {'FINISHED'}



# Main MCell (CellBlender) Properties Class:

class MCellPropertyGroup(bpy.types.PropertyGroup):
    initialized = BoolProperty(
        name="Initialized", default=False)
    cellblender_version = StringProperty(
        name="CellBlender Version", default="0.1.54")
    cellblender_source_hash = StringProperty(
        name="CellBlender Source Hash", default="unknown")
    cellblender_preferences = PointerProperty(
        type=CellBlenderPreferencesPanelProperty,
        name="CellBlender Preferences")
    project_settings = PointerProperty(
        type=MCellProjectPanelProperty, name="CellBlender Project Settings")
    export_project = PointerProperty(
        type=MCellExportProjectPanelProperty, name="Export Simulation")
    run_simulation = PointerProperty(
        type=MCellRunSimulationPanelProperty, name="Run Simulation")
    mol_viz = PointerProperty(
        type=MCellMolVizPanelProperty, name="Mol Viz Settings")
    initialization = PointerProperty(
        type=MCellInitializationPanelProperty, name="Model Initialization")
    partitions = bpy.props.PointerProperty(
        type=MCellPartitionsPanelProperty, name="Partitions")
############# DB: added for parameter import from BNG, SBML models####
    parameters = PointerProperty(
        type=MCellParametersPanelProperty, name="Defined Parameters")
    parameter_system = PointerProperty(
        type=parameter_system.ParameterSystemPropertyGroup, name="Parameter System")
    molecules = PointerProperty(
        type=cellblender_molecules.MCellMoleculesListProperty, name="Defined Molecules")
    reactions = PointerProperty(
        type=MCellReactionsPanelProperty, name="Defined Reactions")
    surface_classes = PointerProperty(
        type=MCellSurfaceClassesPanelProperty, name="Defined Surface Classes")
    mod_surf_regions = PointerProperty(
        type=MCellModSurfRegionsPanelProperty, name="Modify Surface Regions")
    release_patterns = PointerProperty(
        type=MCellReleasePatternPanelProperty, name="Defined Release Patterns")
    release_sites = PointerProperty(
        type=MCellMoleculeReleasePanelProperty, name="Defined Release Sites")
    model_objects = PointerProperty(
        type=MCellModelObjectsPanelProperty, name="Instantiated Objects")
    viz_output = PointerProperty(
        type=MCellVizOutputPanelProperty, name="Viz Output")
    rxn_output = PointerProperty(
        type=MCellReactionOutputPanelProperty, name="Reaction Output")
    meshalyzer = PointerProperty(
        type=MCellMeshalyzerPanelProperty, name="CellBlender Project Settings")
    object_selector = PointerProperty(
        type=MCellObjectSelectorPanelProperty,
        name="CellBlender Project Settings")
    molecule_glyphs = PointerProperty(
        type=MCellMoleculeGlyphsPanelProperty, name="Molecule Shapes")
    scratch_settings = PointerProperty(
        type=MCellScratchPanelProperty, name="CellBlender Scratch Settings")


    def init_properties ( self ):
        self.parameter_system.init_properties()
        self.initialization.init_properties ( self.parameter_system )
        self.molecules.init_properties ( self.parameter_system )
        self.initialized = True


    def draw_uninitialized ( self, layout ):
        row = layout.row()
        row.operator("mcell.init_cellblender", text="Initialize CellBlender")


    def build_data_model_from_properties ( self, context, geometry=False ):
        print ( "build_data_model_from_properties: Constructing a data_model dictionary from current properties" )
        dm = {}
        dm['data_model_version'] = "DM_2014_10_24_1638"
        dm['blender_version'] = [v for v in bpy.app.version]
        dm['cellblender_version'] = self.cellblender_version
        #dm['cellblender_source_hash'] = self.cellblender_source_hash
        dm['cellblender_source_sha1'] = cellblender.cellblender_info["cellblender_source_sha1"]
        if 'api_version' in self:
            dm['api_version'] = self['api_version']
        else:
            dm['api_version'] = 0
        dm['parameter_system'] = self.parameter_system.build_data_model_from_properties(context)
        dm['initialization'] = self.initialization.build_data_model_from_properties(context)
        dm['initialization']['partitions'] = self.partitions.build_data_model_from_properties(context)
        dm['define_molecules'] = self.molecules.build_data_model_from_properties(context)
        dm['define_reactions'] = self.reactions.build_data_model_from_properties(context)
        dm['release_sites'] = self.release_sites.build_data_model_from_properties(context)
        dm['define_release_patterns'] = self.release_patterns.build_data_model_from_properties(context)
        dm['define_surface_classes'] = self.surface_classes.build_data_model_from_properties(context)
        dm['modify_surface_regions'] = self.mod_surf_regions.build_data_model_from_properties(context)
        dm['model_objects'] = self.model_objects.build_data_model_from_properties(context)
        dm['viz_output'] = self.viz_output.build_data_model_from_properties(context)
        dm['reaction_data_output'] = self.rxn_output.build_data_model_from_properties(context)
        if geometry:
            print ( "Adding Geometry to Data Model" )
            dm['geometrical_objects'] = self.model_objects.build_data_model_geometry_from_mesh(context)
            dm['materials'] = self.model_objects.build_data_model_materials_from_materials(context)
        return dm

