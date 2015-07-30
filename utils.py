import os
import bpy


def project_files_path():
    ''' Consolidate the creation of the path to the project files'''

    filepath = os.path.dirname(bpy.data.filepath)
    filepath, dot, blend = bpy.data.filepath.rpartition(os.path.extsep)
    filepath = filepath + "_files"
    filepath = os.path.join(filepath, "mcell")
    return filepath


def preserve_selection_use_operator(operator, new_obj):
    """ Preserve current object selection state and use operator.

    It is not uncommon for Blender operators to make use of the current
    selection. This means you first have to save the current selection state,
    deselect everything, select the object you actually want to do the
    operation on, execute the operator, deselect that object, and finally
    reselect the original selection state. This sounds silly but can be quite
    useful. """

    object_list = bpy.context.scene.objects
    selected_objs = [obj for obj in object_list if obj.select]
    # Deselect everything currently selected, so the operator doesn't act on it
    for obj in selected_objs:
        obj.select = False
    # Select the object we actually want the operator to act on, use it, and
    # deselect.
    new_obj.select = True
    operator()
    new_obj.select = False
    # It's annoying if operators change things they shouldn't, so let's restore
    # the originally select objects.
    for obj in selected_objs:
        obj.select = True


def check_val_str(val_str, min_val, max_val):
    """ Convert val_str to float if possible. Otherwise, generate error. """

    status = ""
    val = None

    try:
        val = float(val_str)
        if min_val is not None:
            if val < min_val:
                status = "Invalid value for %s: %s"
        if max_val is not None:
            if val > max_val:
                status = "Invalid value for %s: %s"
    except ValueError:
        status = "Invalid value for %s: %s"

    return (val, status)



def get_path_to_parent(self_object):
    # Return the Blender class path to the parent object with regard to the Blender Property Tree System
    path_to_self = "bpy.context.scene." + self_object.path_from_id()
    path_to_parent = path_to_self[0:path_to_self.rfind(".")]
    return path_to_parent

def get_parent(self_object):
    # Return the parent Blender object with regard to the Blender Property Tree System
    path_to_parent = get_path_to_parent(self_object)
    parent = eval(path_to_parent)
    return parent

