from __future__ import absolute_import, division, print_function, unicode_literals


from prewikka import version, database, utils, view, error, template, mainmenu

import re

from .graph_generator import Schema 
import pkg_resources

class IODEFNavParameters(mainmenu.MainMenuParameters):
    allow_extra_parameters = True

class IODEFNav(view.View):
    _HTDOCS_DIR = pkg_resources.resource_filename(__name__, 'htdocs')

    plugin_name = "IODEFNav"
    plugin_author = "Sélim Ménouar, Thomas Andrejak"
    plugin_license = version.__license__
    plugin_version = version.__version__
    plugin_copyright = version.__copyright__
    plugin_description = N_("IODEF navigator")
    plugin_htdocs = (("iodefnav", _HTDOCS_DIR),)

    view_parameters = IODEFNavParameters

    def __init__(self):
        view.View.__init__(self)
        self.schema = Schema("%s/yaml" % self._HTDOCS_DIR)

    @view.route("/help/iodefnav", menu=(N_("Help"), N_("IODEF")))
    def render(self):
        iodef_class = env.request.parameters.get("iodef_class", "IODEF-Document")
        dataset = {}

        if iodef_class not in self.schema:
            raise error.PrewikkaUserError(N_("Parameter Error"), N_("%(iodefclass)s is not a valid IODEF class", {'iodefclass':iodef_class}))

        dataset["schema"] = self.schema[iodef_class]
        dataset["full_schema"] = self.schema
        dataset["link"] = self.view_path

        with open("%s/graph/%s.svg" % (self._HTDOCS_DIR, iodef_class), 'r') as stream:
            dataset["svg"] = re.sub(r"\d+pt", "100%", stream.read())

        with open("%s/graph/%s" % (self._HTDOCS_DIR, iodef_class), 'r') as stream:
            dataset["dot"] = stream.read()

        dataset["png"] = "iodefnav/graph/%s.png" % iodef_class

        return template.PrewikkaTemplate(__name__, "templates/iodefnav.mak").render(**dataset)
