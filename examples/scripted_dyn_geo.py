scripted_dyn_geo_dm = {
  'api_version': 0,
  'blender_version': [2, 78, 0],
  'cellblender_version': '0.1.54',
  'cellblender_source_sha1': 'd3b09b9aa9541ae64e57d0ac9646967934623bc2',
  'data_model_version': 'DM_2014_10_24_1638',
  'parameter_system': {
    'model_parameters': [],
    '_extras': {'ordered_id_names': []}
  },
  'define_surface_classes': {
    'surface_class_list': [],
    'data_model_version': 'DM_2014_10_24_1638'
  },
  'define_release_patterns': {
    'data_model_version': 'DM_2014_10_24_1638',
    'release_pattern_list': []
  },
  'mol_viz': {
    'file_index': 1,
    'file_name': 'Scene.cellbin.001.dat',
    'file_start_index': 0,
    'viz_list': ['mol_v'],
    'color_index': 0,
    'file_step_index': 1,
    'viz_enable': True,
    'file_num': 1,
    'file_dir': '',
    'render_and_save': False,
    'seed_list': ['seed_00001'],
    'color_list': [[0.8, 0.0, 0.0], [0.0, 0.8, 0.0], [0.0, 0.0, 0.8], [0.0, 0.8, 0.8], [0.8, 0.0, 0.8], [0.8, 0.8, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0]],
    'manual_select_viz_dir': False,
    'active_seed_index': 0,
    'data_model_version': 'DM_2015_04_13_1700',
    'file_stop_index': 200
  },
  'release_sites': {
    'data_model_version': 'DM_2014_10_24_1638',
    'release_site_list': [
      {
        'pattern': '', 'quantity_type': 'NUMBER_TO_RELEASE', 'molecule': 'v', 'shape': 'CUBIC', 'quantity': '500', 'site_diameter': '1.95', 'release_probability': '1',
        'object_expr': 'ScriptCube', 'stddev': '0', 'orient': "'", 'points_list': [], 'location_y': '0', 'name': 'rel_v', 'data_model_version': 'DM_2015_11_11_1717', 'location_z': '0', 'location_x': '0'
      }
    ]
  },
  'model_objects': {
    'model_object_list': [
      {'script_name': 'dg.py', 'name': 'ScriptCube', 'dynamic': True, 'dynamic_display_source': 'script'}
    ],
    'data_model_version': 'DM_2017_03_16_1750'
  },
  'modify_surface_regions': {'data_model_version': 'DM_2014_10_24_1638', 'modify_surface_regions_list': []},
  'reaction_data_output': {'reaction_output_list': [], 'always_generate': True, 'plot_legend': '0', 'rxn_step': '', 'combine_seeds': True, 'output_buf_size': '', 'mol_colors': False, 'data_model_version': 'DM_2016_03_15_1800', 'plot_layout': ' plot '},
  'initialization': {
    'microscopic_reversibility': 'OFF',
    'interaction_radius': '',
    'surface_grid_density': '10000',
    'radial_directions': '',
    'center_molecules_on_grid': False,
    'time_step': '1e-6',
    'space_step': '',
    'export_all_ascii': False,
    'partitions': {'y_end': '1', 'z_step': '0.02', 'x_start': '-1', 'x_end': '1', 'x_step': '0.02', 'recursion_flag': False, 'include': False, 'z_start': '-1', 'y_start': '-1', 'data_model_version': 'DM_2016_04_15_1600', 'y_step': '0.02', 'z_end': '1'},
    'radial_subdivisions': '',
    'time_step_max': '',
    'vacancy_search_distance': '',
    'iterations': '200',
    'accurate_3d_reactions': True,
    'data_model_version': 'DM_2014_10_24_1638',
    'warnings': {
      'missed_reaction_threshold': '0.001', 'negative_reaction_rate': 'WARNING', 'all_warnings': 'INDIVIDUAL', 'degenerate_polygons': 'WARNING', 'missed_reactions': 'WARNING', 'useless_volume_orientation': 'WARNING', 'high_probability_threshold': '1',
      'lifetime_threshold': '50', 'missing_surface_orientation': 'ERROR', 'negative_diffusion_constant': 'WARNING', 'high_reaction_probability': 'IGNORED', 'lifetime_too_short': 'WARNING'
    },
    'notifications': {
      'release_event_report': True, 'all_notifications': 'INDIVIDUAL', 'molecule_collision_report': False, 'iteration_report': True, 'varying_probability_report': True, 'probability_report': 'ON', 'partition_location_report': False,
      'diffusion_constant_report': 'BRIEF', 'box_triangulation_report': False, 'probability_report_threshold': '0', 'file_output_report': False, 'final_summary': True, 'progress_report': True
    }
  },
  'simulation_control': {'start_seed': '1', 'processes_list': [], 'run_limit': '-1', 'end_seed': '1', 'name': '', 'data_model_version': 'DM_2016_10_27_1642'},
  'materials': {'material_dict': {'ScriptCube_mat': {'diffuse_color': {'a': 0.2, 'g': 0.8, 'r': 0.0, 'b': 0.12}}}},
  'scripting': {'force_property_update': True, 'show_data_model_scripting': True, 'dm_internal_file_name': '', 'dm_external_file_name': '',
    'script_texts': {
      'dg.py': "# This script gets both its inputs and outputs from the environment:\n" \
               "#\n" \
               "#  frame_number is the frame number indexed from the start of the simulation\n" \
               "#  time_step is the amount of time between each frame (same as CellBlender's time_step)\n" \
               "#  points[] is a list of points where each point is a list of 3 doubles: x, y, z\n" \
               "#  faces[] is a list of faces where each face is a list of 3 integer indexes of points (0 based)\n" \
               "#  origin[] contains the x, y, and z values for the center of the object (points are relative to this).\n" \
               "#\n" \
               "# This script must fill out the points and faces lists for the time given by frame_number and time_step.\n" \
               "# CellBlender will call this function repeatedly to create the dynamic MDL and possibly during display.\n" \
               "\n" \
               "import math\n" \
               "\n" \
               "points.clear()\n" \
               "faces.clear()\n" \
               "\n" \
               "min_ztop = 1.0\n" \
               "max_ztop = 4.0\n" \
               "period_frames = 100\n" \
               "\n" \
               "sx = sy = sz = 1\n" \
               "h = ( 1 + math.sin ( math.pi * ((2*frame_number/period_frames) - 0.5) ) ) / 2\n" \
               "\n" \
               "zt = min_ztop + ( (max_ztop-min_ztop) * h )\n" \
               "\n" \
               "# These define the coordinates of the rectangular box\n" \
               "points.append ( [  sx,  sy, -sz ] )\n" \
               "points.append ( [  sx, -sy, -sz ] )\n" \
               "points.append ( [ -sx, -sy, -sz ] )\n" \
               "points.append ( [ -sx,  sy, -sz ] )\n" \
               "points.append ( [  sx,  sy,  zt ] )\n" \
               "points.append ( [  sx, -sy,  zt ] )\n" \
               "points.append ( [ -sx, -sy,  zt ] )\n" \
               "points.append ( [ -sx,  sy,  zt ] )\n" \
               "\n" \
               "# These define the faces of the rectangular box\n" \
               "faces.append ( [ 1, 2, 3 ] )\n" \
               "faces.append ( [ 7, 6, 5 ] )\n" \
               "faces.append ( [ 4, 5, 1 ] )\n" \
               "faces.append ( [ 5, 6, 2 ] )\n" \
               "faces.append ( [ 2, 6, 7 ] )\n" \
               "faces.append ( [ 0, 3, 7 ] )\n" \
               "faces.append ( [ 0, 1, 3 ] )\n" \
               "faces.append ( [ 4, 7, 5 ] )\n" \
               "faces.append ( [ 0, 4, 1 ] )\n" \
               "faces.append ( [ 1, 5, 2 ] )\n" \
               "faces.append ( [ 3, 2, 7 ] )\n" \
               "faces.append ( [ 4, 0, 7 ] )\n" \
               "" },
    'scripting_list': [], 'show_simulation_scripting': False, 'data_model_version': 'DM_2016_03_15_1900'
  },
  'define_molecules': {
    'data_model_version': 'DM_2014_10_24_1638',
    'molecule_list': [
      {
        'display': {'color': [0.0, 1.0, 0.0], 'emit': 0.0, 'glyph': 'Sphere_1', 'scale': 10.0},
        'target_only': False, 'maximum_step_length': '', 'diffusion_constant': '1e-3', 'mol_type': '3D', 'export_viz': False,
        'custom_time_step': '', 'data_model_version': 'DM_2016_01_13_1930', 'mol_name': 'v', 'mol_bngl_label': '', 'custom_space_step': ''
      }
    ]
  },
  'viz_output': {
    'export_all': True, 'step': '1', 'start': '0', 'data_model_version': 'DM_2014_10_24_1638', 'all_iterations': True, 'end': '1'
  },
  'geometrical_objects': {
    'object_list': [
      {
        'name': 'ScriptCube',
        'element_connections': [[1, 2, 3], [7, 6, 5], [4, 5, 1], [5, 6, 2], [2, 6, 7], [0, 3, 7], [0, 1, 3], [4, 7, 5], [0, 4, 1], [1, 5, 2], [3, 2, 7], [4, 0, 7]],
        'location': [0.0, 0.0, 0.0],
        'vertex_list': [[1.0, 1.0, -1.0], [1.0, -1.0, -1.0], [-1.0, -1.0, -1.0], [-1.0, 1.0, -1.0], [1.0, 1.0, 1.3], [1.0, -1.0, 1.3], [-1.0, -1.0, 1.3], [-1.0, 1.0, 1.3]],
        'material_names': ['ScriptCube_mat']
      }
    ]
  },
  'define_reactions': {'data_model_version': 'DM_2014_10_24_1638', 'reaction_list': []}
}

