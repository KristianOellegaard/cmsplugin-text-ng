from django.apps import AppConfig

from cmsplugin_text_ng.type_registry import register_type


class CmsPluginTextNgConfig(AppConfig):
    name = 'cmsplugin_text_ng'
    verbose_name = "Django Cms Plugin Text-NG"

    def ready(self):
        from cmsplugin_text_ng.models import TextNGVariableText
        register_type('text', TextNGVariableText)
