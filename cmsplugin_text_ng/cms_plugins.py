from collections import defaultdict
from django.template.loader import get_template
from django.contrib.admin import StackedInline
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict

from cms.plugin_pool import plugin_pool
from cmsplugin_text_ng.forms import PluginAddForm, PluginEditForm

from cmsplugin_text_ng.compat import TextPlugin
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

    def get_inline_instances(self, request, obj=None):
        inline_instances = []

        if obj and obj.pk:
            variables = get_variables_from_template(obj.template.path).items()
            types = SortedDict()
            for label, variable in variables:
                types[variable['type']] = types.get(variable['type'], 0)  # can't use defaultdict :(
                types[variable['type']] += 1
                variable['type'].objects.get_or_create(text_ng=obj, label=label)

            for model_class in types.keys():
                inline = self.get_inline_for_model(model_class)
                inline.max_num = types[model_class]
                inline_instances.append(inline(self.model, self.admin_site))
        return inline_instances

    def render(self, context, instance, placeholder):
        context = super(TextPluginNextGeneration, self).render(context, instance, placeholder)
        template = get_template(instance.template.path)
        variables = get_variables_from_template(template)
        for label, variable in variables.items():
            model_type = variable['type']
            var, created = model_type.objects.select_related(*model_type.select_related).get_or_create(text_ng=instance, label=label)
            context[label] = var.value
        context.update({'body': mark_safe(template.render(context))})
        return context


plugin_pool.register_plugin(TextPluginNextGeneration)
