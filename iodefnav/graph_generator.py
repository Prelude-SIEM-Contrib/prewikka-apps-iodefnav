#!/usr/bin/env python
# -*- coding: utf8 -*-

import glob
import json
import yaml
import cgi
from io import open

try:
    import graphviz
    WITH_GRAPHVIZ = True
except ImportError:
    WITH_GRAPHVIZ = False

class Schema(dict):
    def __init__(self, folder, ext='*'):
        self.folder = folder
        self.ext = ext
        for struct in self.load(folder, ext):
            self[struct["name"]] = struct

    @classmethod
    def load(cls, folder, ext='*'):
        mapping = {
            'json': json.load,
            'yml': yaml.load
        }

        for f in glob.glob("%s/*.%s" % (folder, ext)):
            extension = f.split('.')[-1]

            if extension not in mapping:
                continue

            with open(f, 'r', encoding='utf-8') as stream:
                yield mapping[extension](stream)

    def graphviz(self, iodef_class, direction='LR', link_format=None, format='svg'):
        dot = graphviz.Graph(comment=iodef_class, format=format)
        dot.graph_attr['rankdir'] = direction
        dot.node_attr['shape'] = 'plaintext'

        self.add_node(dot, iodef_class, link_format)

        return dot

    def svg(self, iodef_class, direction='LR', link_format=None):
        dot = self.graphviz(iodef_class, direction, link_format, format='svg')

        return dot.pipe().decode('utf-8')

    def gen_all(self, directory, direction='LR', link_format=None, out_format=None):
        for name in self.keys():
            if not out_format:
                for format in ('svg', 'png'):
                    self.graphviz(name, direction, link_format, format).render(name, directory)

                continue

            self.graphviz(name, direction, link_format, out_format).render(name, directory)


    def add_node(self, dot, node_name, link_format=None, nodes=None):
        if node_name not in self:
            return

        if not nodes:
            nodes = {}

        nodes[node_name] = True

        color = self[node_name].get("color", "#FFFFFF")
        link = link_format % node_name if link_format else "#"

        label = """<
        <table BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <tr>
            <td BGCOLOR="{color}" HREF="{link}" TITLE="{title}">{name}</td>
        </tr>
        """.format(
            color=self.darken_color(color),
            link=link,
            title=cgi.escape(self[node_name].get("description"), quote=True),
            name=node_name
        )

        for key, value in self[node_name].get("childs", {}).items():
            if key not in self:
                continue

            if key not in nodes:
                self.add_node(dot, key, link_format, nodes)

            dot.edge(node_name, key, label=value.get("multiplicity"), dir="back", arrowtail="invempty")

        for key, value in self[node_name].get("aggregates", {}).items():
            if key in self:
                if key not in nodes:
                    self.add_node(dot, key, link_format, nodes)

                dot.edge(node_name, key, label=value.get("multiplicity"), dir="forward")
                continue

            label += self.graph_attr(key, value, color, link)

        for key, value in self[node_name].get("attributes", {}).items():
            label += self.graph_attr(key, value, color, link)

        label += "</table>>"
        dot.node(node_name, label)

    @staticmethod
    def darken_color(hex_color, amount=0.6):
        hex_color = hex_color.replace('#', '')
        rgb = []
        rgb.append(int(hex_color[0:2], 16) * amount)
        rgb.append(int(hex_color[2:4], 16) * amount)
        rgb.append(int(hex_color[4:6], 16) * amount)

        return "#" + ''.join(["{0:02x}".format(int(c)) for c in rgb])

    @staticmethod
    def graph_attr(name, value, color, link):
        return """<tr><td BGCOLOR="{color}" HREF="{link}" TITLE="{title}" >[{type}] {name} ({mult})</td></tr>""".format(
            color=color,
            link=link,
            title=cgi.escape(value.get("description"), quote=True),
            name=name,
            mult=value.get("multiplicity"),
            type=value.get("type"),
        )

if __name__ == "__main__":
    schema = Schema('htdocs/yaml')
    schema.gen_all("htdocs/graph", link_format="/help/iodefnav?iodef_class=%s")

