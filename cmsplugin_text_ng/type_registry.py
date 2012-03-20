# -*- coding: utf-8 -*-
from django.db.models import FieldDoesNotExist

from cmsplugin_text_ng import exceptions

_registry = {}

def register_type(type_name, model_class):
    from cmsplugin_text_ng.models import TextNGVariableBase
    if type_name in _registry:
        if _registry[type_name] == model_class:
            # already registered
            return
        else:
            raise exceptions.VariableTypeAlreadyRegistered(
                'The type "%s" is already registered by %s' % (type_name, _registry[type_name].__name__)
            )
    if not issubclass(model_class, TextNGVariableBase):
        raise exceptions.InvalidType('%s is not a subclass of TextNGVariableBase' % model_class.__name__)
    try:
        field = model_class._meta.get_field_by_name('value')[0]
    except FieldDoesNotExist:
        raise exceptions.InvalidType('%s does not define a "value" field' % model_class.__name__)
    if not field.null:
        raise exceptions.InvalidType('"value" field of %s is not nullable' % model_class.__name__)
    _registry[type_name] = model_class

def get_type(type_name):
    return _registry[type_name]

def get_type_list():
    return _registry.values()