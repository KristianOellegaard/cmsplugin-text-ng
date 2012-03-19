from collections import defaultdict
from django import template
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from cms.plugins.text.cms_plugins import TextPlugin
from cms.plugin_pool import plugin_pool
from cmsplugin_text_ng.forms import PluginAddForm, PluginEditForm

from cmsplugin_text_ng.models import TextNG
from cmsplugin_text_ng.utils import get_variables_from_template
from cmsplugin_text_ng import type_registry


class TextPluginNextGeneration(TextPlugin):
    model = TextNG
    name = _("Text NG")
    form = PluginEditForm

    def __init__(self, model=None,  admin_site=None):
        self.inlines = []
        for model_class in type_registry.get_type_list():
            class TypeStackedInline(StackedInline):
                model = model_class
                extra = 0
                can_delete = False
                readonly_fields = ('label',)
            self.inlines.append(TypeStackedInline)
        super(TextPluginNextGeneration, self).__init__(model, admin_site)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return PluginAddForm
        else:
            return super(TextPluginNextGeneration, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super(TextPluginNextGeneration, self).save_model(request, obj, form, change)
        for label, variable in get_variables_from_template(obj.template.path).items():
            variable['type'].objects.get_or_create(text_ng=obj, label=label)

    def get_formsets(self, request, obj=None):
        if not obj:
            raise StopIteration()
        types = defaultdict(lambda: 0)
        for label, variable in get_variables_from_template(obj.template.path).items():
            types[variable['type']] += 1
        for inline in self.inline_instances:
            if inline.model in types:
                inline.max_num = types[inline.model]
                yield inline.get_formset(request, obj)

    def render(self, context, instance, placeholder):
        context = super(TextPluginNextGeneration, self).render(context, instance, placeholder)
        t = template.loader.get_template(instance.template.path)
        variables = get_variables_from_template(t)
        for label, variable in variables.items():
            model_type = variable['type']
            var, created = model_type.objects.select_related(*model_type.select_related).get_or_create(text_ng=instance, label=label)
            context[label] = var.value
        context.update({'body': mark_safe(t.render(context))})
        return context


plugin_pool.register_plugin(TextPluginNextGeneration)