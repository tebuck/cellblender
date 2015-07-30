import sys
import os
import hashlib

cellblender_info = {
    "supported_version_list": [(2, 73, 0),(2, 74, 0),(2, 75, 0)],

    #######################################################################################
    ### Note that cellblender_id.py is NOT in this list because it is autogenerated!!!! ###
    #######################################################################################
    "cellblender_source_list": [
        "__init__.py",
        "cellblender_source_info.py",
        "data_model.py",
        "parameter_system.py",
        "cellblender_properties.py",
        "cellblender_panels.py",
        "cellblender_operators.py",
        "cellblender_molecules.py",
        "cellblender_reactions.py",
        "cellblender_release.py",
        "cellblender_surface_classes.py",
        "cellblender_partitions.py",
        "object_surface_regions.py",
        "run_simulations.py",
        "sim_runner_queue.py",
        "run_wrapper.py",

        "icons"+os.sep+"cellblender_icon.png",
        "icons"+os.sep+"mol_sel.png",
        "icons"+os.sep+"mol_unsel.png",
        "icons"+os.sep+"reactions_sel.png",
        "icons"+os.sep+"reactions_unsel.png",

        "developer_utilities"+os.sep+"data_model_print.py",
        "developer_utilities"+os.sep+"data_model_pyedit.py",
        "developer_utilities"+os.sep+"data_model_tree.py",

        "SimControl.java",
        "META-INF"+os.sep+"MANIFEST.MF",
#        "SimControl.jar",
#        "SimControl.c",
#        "SimControl",

        "cellblender_utils.py",
        "glyph_library.blend",
        "io_mesh_mcell_mdl"+os.sep+"__init__.py",
        "io_mesh_mcell_mdl"+os.sep+"export_mcell_mdl.py",
        "io_mesh_mcell_mdl"+os.sep+"import_mcell_mdl.py",
        "io_mesh_mcell_mdl"+os.sep+"import_mcell_mdl_pyparsing.py",
        "io_mesh_mcell_mdl"+os.sep+"import_shared.py",
        "io_mesh_mcell_mdl"+os.sep+"pyparsing.py",
#        "io_mesh_mcell_mdl"+os.sep+"mdlmesh_parser.py",
        "io_mesh_mcell_mdl"+os.sep+"mdlobj.py",
        "data_plotters"+os.sep+"__init__.py",
        "data_plotters"+os.sep+"mpl_simple"+os.sep+"__init__.py",
        "data_plotters"+os.sep+"mpl_simple"+os.sep+"mpl_simple.py",
        "data_plotters"+os.sep+"mpl_plot"+os.sep+"__init__.py",
        "data_plotters"+os.sep+"mpl_plot"+os.sep+"mpl_plot.py",
        "data_plotters"+os.sep+"mpl_plot"+os.sep+"mpl_defaults.py",
        "data_plotters"+os.sep+"xmgrace"+os.sep+"__init__.py",
        "data_plotters"+os.sep+"java_plot"+os.sep+"__init__.py",
        "data_plotters"+os.sep+"java_plot"+os.sep+"PlotData.java",
        "data_plotters"+os.sep+"java_plot"+os.sep+"META-INF"+os.sep+"MANIFEST.MF",
#        "data_plotters"+os.sep+"java_plot"+os.sep+"PlotData.jar",
        "mdl"+os.sep+"__init__.py",
        "bng"+os.sep+"__init__.py",
        "bng"+os.sep+"sbml2blender.py",
        "bng"+os.sep+"sbml2json.py",
        "bng"+os.sep+"external_operators.py",
        "bng"+os.sep+"sbml_operators.py",
        "bng"+os.sep+"sbml_properties.py",
        "bng"+os.sep+"bng_operators.py",
        "bng"+os.sep+"treelib3"+os.sep+"__init__.py",
        "bng"+os.sep+"treelib3"+os.sep+"node.py",
        "bng"+os.sep+"treelib3"+os.sep+"tree.py",
        "bng"+os.sep+"libsbml3"+os.sep+"__init__.py",
        ],

    "cellblender_source_sha1": "",
    "versions_match": False,
    "cellblender_addon_path": "",
    "cellblender_plotting_modules": []
}


def identify_source_version(addon_path,verbose=False):
    """ Compute the SHA1 of all source files in cellblender_info["cellblender_source_list"] 
        and save in cellblender_info['cellblender_source_sha1']"""
    cbsl = cellblender_info["cellblender_source_list"]
    hashobject = hashlib.sha1()
    for source_file_basename in cbsl:
        source_file_name = os.path.join(addon_path, source_file_basename)
        if os.path.isfile(source_file_name):
            hashobject.update(open(source_file_name, 'rb').read())  # .encode("utf-8"))
            if verbose:
                print("  Cumulative SHA1 = " + str(hashobject.hexdigest()) + " after adding " + source_file_name )
        else:
            # This is mainly needed in case the make file wasn't run. 
            # (i.e. missing mdlmesh_parser.py)
            if verbose:
                print('  File "%s" does not exist' % source_file_name)

    cellblender_info['cellblender_source_sha1'] = hashobject.hexdigest()


def identify_source_version_from_file():
    """ Return the SHA1 found in "cellblender_id.py" and save in cellblender_info['cellblender_source_sha1'] """
    cs = open ( os.path.join(os.path.dirname(__file__), 'cellblender_id.py') ).read()
    cellblender_info['cellblender_source_sha1'] = cs[1+cs.find("'"):cs.rfind("'")]
    return ( cellblender_info['cellblender_source_sha1'] )


def print_source_list (addon_path,verbose=False):
    """ Compute the SHA1 of all source files in cellblender_info["cellblender_source_list"]"""
    cbsl = cellblender_info["cellblender_source_list"]
    ### Note that cellblender_id.py is NOT in the normal source list and must be added manually!!!!
    ### print( "cellblender" + os.sep + "cellblender_id.py" )
    for source_file in cbsl:
        if os.path.isfile(source_file):
            print( "cellblender" + os.sep + source_file )


if __name__ == '__main__':

    """Run this file from the command line to print the file list and update the cellblender_id.py file."""

    id_file_name = "cellblender_id.py"
    identify_source_version(os.path.dirname(__file__),verbose=False)
    
    cb_id_statement = "cellblender_id = '" + cellblender_info['cellblender_source_sha1'] + "'\n"
    sha_file_name = os.path.join(os.path.dirname(__file__), id_file_name)
    rebuild = True
    if os.path.exists(sha_file_name):
        sha_file = open(sha_file_name, 'r')
        current_statement = sha_file.read()
        sha_file.close()
        if current_statement.strip() == cb_id_statement.strip():
            rebuild = False
    
    if rebuild:
        open(sha_file_name, 'w').write(cb_id_statement)

    print_source_list(os.path.dirname(__file__))
    import sys
    sys.exit(0)

