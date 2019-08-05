import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import mimetypes
import ckan.lib.base as base
import ckan.lib.helpers as helpers
from flask import Blueprint
import ckan.model as model
from ckan.common import g, _
import ckan.logic as logic
import logging

log = logging.getLogger(__name__)
NotAuthorized = logic.NotAuthorized


def view_file(pkg_id, resource_id):
    # check access to the resource
    try:
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'for_view': True,
            u'auth_user_obj': g.userobj
        }
        helpers.check_access(u'resource_show', {'id': resource_id})
    except NotAuthorized:
        base.abort(403, _(u'Not authorized to view this resource'))
    resource = toolkit.get_action('resource_show')(context, {'id': resource_id, 'include_tracking': False})
    # use the correct javascript file to render the data for the resource's format
    if (resource["format"].lower() == "stl"):
        return base.render("vtkjs_view_stl.html", extra_vars={'url': resource["url"]})
    else:
        return base.render("vtkjs_view_vtk.html", extra_vars={'url': resource["url"]})


class VtkjsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        # add mimetypes so that viewable file formats are recognized
        mimetypes.add_type("STL", ".stl")
        mimetypes.add_type("VTK", ".vtk")

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'vtkjs')

    # IResourceView

    def info(self):
        return {"name": "vtkjs",
                "title": toolkit._("VTK and STL Viewer"),
                "icon": "cube",
                "default_title": toolkit._("VTK and STL Viewer"),
                "iframed": False}

    def can_view(self, data_dict):
        resource = data_dict["resource"]
        return (resource.get('format', '').lower() in ['stl', 'vtk'])

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
