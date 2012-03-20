# -*- coding: utf-8 -*-
from functools import wraps

from django.template import loader, TemplateSyntaxError

from cmsplugin_text_ng.templatetags.text_ng_tags import DefineNode
from cmsplugin_text_ng.type_registry import get_type

def ensure_template_arg(func):
    def _dec(template):
        if isinstance(template, basestring):
            template = loader.get_template(template)
        return func(template)
    return wraps(func)(_dec)

@ensure_template_arg
def get_variables_from_template(template):
    variable_nodes = [n for n in template.nodelist if isinstance(n, DefineNode)]
    variables = {}
    for node in variable_nodes:
        if node.variable_name in variables:
            raise TemplateSyntaxError('%s defined multiple times - %s' % (
                node.variable_name,
                _get_template_name_from_node(node)
            ))
        try:
            variables[node.variable_name] = {
                'type': get_type(node.variable_type),
                'optional': node.optional,
            }
        except KeyError:
            raise TemplateSyntaxError('%s type not registered - %s' % (
                node.variable_type,
                _get_template_name_from_node(node)
            ))
    return variables

def _get_template_name_from_node(node):
    try:
        return node.source[0].name
    except Exception:
        return ''