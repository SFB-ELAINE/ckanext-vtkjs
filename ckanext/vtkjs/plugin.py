import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import mimetypes
import ckan.lib.base as base
import ckan.lib.helpers as helpers
from flask import Blueprint
import ckan.model as model
from ckan.common import g
import ckan.logic as logic
import logging
import zipfile

log = logging.getLogger(__name__)
NotAuthorized = logic.NotAuthorized


def get_filepath(resource_id):
    '''
    Returns the path to the location of the file associated with
    the resource with the given resource ID.
    '''
    return "/var/lib/ckan/default/resources/" + resource_id[0:3] + \
        "/" + resource_id[3:6] + "/" + resource_id[6:]


def view_file(pkg_id, resource_id):
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': g.user,
        u'for_view': True,
        u'auth_user_obj': g.userobj
    }
    # check access to the resource
    ret = helpers.check_access(u'resource_show', {'id': resource_id})
    if not ret:
        return base.render("not_authorized.html")

    resource = toolkit.get_action('resource_show')(context, {'id': resource_id, 'include_tracking': False})
    # use the correct javascript file to render the data for the resource's format
    if (resource["format"].lower() == "stl"):
        return base.render("vtkjs_view_stl.html", extra_vars={'url': resource["url"]})
    elif resource["format"].lower() == "vtp":
        return base.render("vtkjs_view_vtp.html", extra_vars={'url': resource["url"]})
    elif resource["format"].lower() == "vti":
        return base.render("vtkjs_view_vti.html", extra_vars={'url': resource["url"]})
    elif resource["format"].lower() == "zip":
        return base.render("vtkjs_view_obj-zip.html", extra_vars={'url': resource["url"]})


class VtkjsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IResourceController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        # add mimetypes so that viewable file formats are recognized
        mimetypes.add_type("STL", ".stl")
        mimetypes.add_type("VTK", ".vtk")
        mimetypes.add_type("VTI", ".vti")
        mimetypes.add_type("VTP", ".vtp")
        mimetypes.add_type("OBJ", ".obj")

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'vtkjs')

    # IResourceView

    def info(self):
        return {"name": "vtkjs",
                "title": toolkit._("3D Viewer"),
                "icon": "cube",
                "default_title": toolkit._("3D Viewer"),
                "iframed": False}

    def can_view(self, data_dict):
        resource = data_dict["resource"]
        return (resource.get('format', '').lower() in ['stl', 'vtp', 'vti', 'zip'])

    def setup_template_variables(self, context, data_dict):
        return data_dict

    def view_template(self, context, data_dict):
        return "view.html"

    def form_template(self, context, data_dict):
        return "vtkjs_form.html"

    # IBlueprint

    def get_blueprint(self):
        blueprint = Blueprint('vtkjs', self.__module__)
        # blueprint.add_url_rule(u'/dataset/<pkg_id>/resource/<filename>/paraview', 'resource_paraview', resource_paraview)
        blueprint.add_url_rule(u'/dataset/<pkg_id>/resource/<resource_id>/vtkjs', 'vtkjs', view_file)
        return blueprint

    # IResourceController

    def after_create(self, context, resource):
        # check if the resource has a .vtk extension but is actually a Polydata file
        # if it is, we can display it
        src = get_filepath(resource["id"])
        if resource["format"].lower() == "vtk":
            # check if it's a polydata
            f = open(src, "r")
            for line in f:
                if(line[0:8] == "DATASET "):
                    if (line[8:-1] == "POLYDATA"):
                        resource["format"] = "VTP"
                        resource = toolkit.get_action('resource_update')(context, resource)
                    else:
                        log.info(line[8:-1])
                    break
            f.close()

        found_obj = False
        if resource["format"].lower() == "zip":
            with zipfile.ZipFile(src, 'r') as zip_ref:
                for item in zip_ref.namelist():
                    if item[-4:] == ".obj":
                        found_obj = True
        if found_obj or resource["format"].lower() == "vtp" or \
                resource["format"].lower() == "vti" or \
                resource["format"].lower() == "stl":
            toolkit.get_action('resource_view_create')(context, {
                                    'resource_id': resource['id'],
                                    'title': '3D Viewer',
                                    'view_type': 'vtkjs'
                                    })
        return resource
