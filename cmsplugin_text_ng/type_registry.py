# -*- coding: utf-8 -*-

_registry = {}

class VariableTypeAlreadyRegistered(Exception):
    pass


class InvalidType(Exception):
    pass

def register_type(type_name, model_class):
    from cmsplugin_text_ng.models import TextNGVariableBase
    if type_name in _registry:
        if _registry[type_name] == model_class:
            # already registered
            return
        else:
            raise VariableTypeAlreadyRegistered(
                'The type "%s" is already registered by %s' % (type_name, _registry[type_name].__name__)
            )
    if not issubclass(model_class, TextNGVariableBase):
        raise InvalidType('%s is not a subclass of TextNGVariableBase' % model_class.__name__)
    # TODO: validate that there is a "value" field that is nullable
    _registry[type_name] = model_class

def get_type(type_name):
    return _registry[type_name]

def get_type_list():
    return _registry.values()