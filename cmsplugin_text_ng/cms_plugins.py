from cms.plugins.text.cms_plugins import TextPlugin
from cmsplugin_text_ng.models import TextNG
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from django import template
from django.template.context import Context
from django.utils.safestring import mark_safe

class TextPluginNextGeneration(TextPlugin):
    model = TextNG
    name = _("Text NG")

    def render(self, context, instance, placeholder):
        context = super(TextPluginNextGeneration, self).render(context, instance, placeholder)
        t = template.loader.get_template(instance.template.path)
        context.update({'body': mark_safe(t.render(Context(context)))})
        return context


plugin_pool.register_plugin(TextPluginNextGeneration)