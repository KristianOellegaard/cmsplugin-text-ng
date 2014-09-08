# -*- coding: utf-8 -*-
from django import template
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs

register = template.Library()


class DefineNode(template.Node):

    def __init__(self, variable_name, variable_type, optional=False, initial_values=None):
        if initial_values is None:
            initial_values = {}

        self.variable_name = variable_name
        self.variable_type = variable_type
        self.optional = optional
        self.initial_field_values = initial_values

    def render(self, context):
        """
        This template tag does not materialize itself in the template
        """
        return ''


error_message = 'Syntax: {% define variable_name as variable_type [optional] with field=value %}'

@register.tag(name='define')
def do_define(parser, token):
    bits = token.split_contents()[1:]
    initial_values = None

    if len(bits) < 3 and bits[1] != 'as':
        raise template.TemplateSyntaxError(error_message)

    del bits[1] # "as"

    try:
        variable_name, variable_type = bits[:2]
    except ValueError:
        raise TemplateSyntaxError(error_message)

    try:
        optional = bits[2] == 'optional'
    except IndexError:
        optional = False

    if not optional and 'optional' in bits:
        raise TemplateSyntaxError(error_message)

    try:
        if optional:
            index = 3
        else:
            index = 2

        with_tag = bits[index]
        assert with_tag, 'with'
        bits = bits[index + 1:]
    except IndexError:
        pass
    except AssertionError:
        raise TemplateSyntaxError(error_message)
    else:
        initial_values = token_kwargs(bits, parser, support_legacy=False)

        if not initial_values:
            raise TemplateSyntaxError(error_message)

        for var, val in initial_values.items():
            initial_values[var] = val.resolve({}) # nasty, don't have access to context.

    return DefineNode(variable_name, variable_type, optional, initial_values)
