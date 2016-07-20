import pkg_resources

from prewikka import database, env, utils, view, error
from . import templates

import json
import re

import graph_generator

class IODEFNav(view.View):
    class IODEFNavParameters(view.Parameters):
        def register(self):
            self.optional("iodef_class", str, default="IODEF-Document")

    _HTDOCS_DIR = pkg_resources.resource_filename(__name__, 'htdocs')


    plugin_name = "IODEFNav"
    plugin_author = "Sélim Menouar"
    plugin_license = "GPL"
    plugin_version = "1.0.0"
    plugin_copyright = "CSSI"
    plugin_description = "IODEF navigator"
    plugin_htdocs = (("iodefnav", _HTDOCS_DIR),)
    view_template = templates.iodefnav
    view_parameters = IODEFNavParameters
    view_name = N_("IODEF")
    view_section = N_("Help")

    def __init__(self):
        view.View.__init__(self)
        self.schema = graph_generator.Schema("%s/yaml" % self._HTDOCS_DIR)

    def render(self):
        iodef_class = self.parameters["iodef_class"]

        if iodef_class not in self.schema:
            raise error.PrewikkaUserError("Parameter Error", _("%s is not a valid IODEF class") % iodef_class)

        self.dataset["schema"] = self.schema[iodef_class]
        self.dataset["full_schema"] = self.schema
        self.dataset["link"] = self.view_path

        with open("%s/graph/%s.svg" % (self._HTDOCS_DIR, iodef_class), 'r') as stream:
            self.dataset["svg"] = re.sub(r"\d+pt", "100%", stream.read())

        with open("%s/graph/%s" % (self._HTDOCS_DIR, iodef_class), 'r') as stream:
            self.dataset["dot"] = stream.read()

        self.dataset["png"] = "iodefnav/graph/%s.png" % iodef_class

