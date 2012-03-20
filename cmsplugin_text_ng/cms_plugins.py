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


class TextPluginNextGeneration(TextPlugin):
    model = TextNG
    name = _("Text NG")
    form = PluginEditForm

    def get_inline_for_model(self, model_class):
        attrs = {
            'model': model_class,
            'extra': 0,
            'can_delete': False,
            'readonly_fields': ('label',),
        }
        return type('%sTypeStackedInline' % model_class.__name__, (StackedInline,), attrs)

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return PluginAddForm
        else:
            return super(TextPluginNextGeneration, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super(TextPluginNextGeneration, self).save_model(request, obj, form, change)
        for label, variable in get_variables_from_template(obj.template.path).items():
            variable['type'].objects.get_or_create(text_ng=obj, label=label)

    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        types = defaultdict(lambda: 0)
        for label, variable in get_variables_from_template(obj.template.path).items():
            types[variable['type']] += 1
            variable['type'].objects.get_or_create(text_ng=obj, label=label)
        self.inline_instances = []
        self.inlines = []
        for model_class in types.keys():
            inline = self.get_inline_for_model(model_class)
            inline.max_num = types[model_class]
            self.inlines.append(inline)
            self.inline_instances.append(inline(self.model, self.admin_site))
        return super(TextPluginNextGeneration, self).change_view(request, object_id, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        self.inline_instances = []
        return super(TextPluginNextGeneration, self).add_view(request, form_url, extra_context)

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