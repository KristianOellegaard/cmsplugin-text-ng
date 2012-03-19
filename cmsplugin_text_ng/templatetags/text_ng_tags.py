# -*- coding: utf-8 -*-
from django import template

register = template.Library()


class DefineNode(template.Node):
    def __init__(self, variable_name, variable_type, optional=False):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.optional = optional

    def render(self, context):
        """
        This template tag does not materialize itself in the template
        """
        return ''


error_message = 'Syntax: {% define variable_name as variable_type [optional] %}'

@register.tag(name='define')
def do_define(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) < 3 and bits[1] != 'as':
        raise template.TemplateSyntaxError(error_message)
    del bits[1] # "as"
    if len(bits) == 2:
        variable_name, variable_type = bits
        optional = False
    elif len(bits) == 3:
        if bits[2] == 'optional':
            variable_name, variable_type = bits[:2]
            optional = True
        else:
            raise template.TemplateSyntaxError(error_message)
    else:
        raise template.TemplateSyntaxError(error_message)
    return DefineNode(variable_name, variable_type, optional)
