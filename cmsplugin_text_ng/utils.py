# -*- coding: utf-8 -*-
from django.template import loader

from cmsplugin_text_ng.templatetags.text_ng_tags import DefineNode
from cmsplugin_text_ng.type_registry import get_type

def get_variables_from_template(template):
    if isinstance(template, basestring):
        template = loader.get_template(template)
    variable_nodes = [n for n in template.nodelist if isinstance(n, DefineNode)]
    variables = {}
    for node in variable_nodes:
        variables[node.variable_name] = {
            'type': get_type(node.variable_type),
            'optional': node.optional,
        }
    return variables