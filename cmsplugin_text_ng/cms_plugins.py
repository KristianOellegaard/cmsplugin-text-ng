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

    def get_inline_instances(self, request, obj=None):
        inline_instances = []

        if obj and obj.pk:
            variables = get_variables_from_template(obj.template.path).items()
            types = SortedDict()
            for label, variable in variables:
                model_class = variable['type']
                initial_field_values = variable['initial_field_values']
                types[model_class] = types.get(model_class, 0)  # can't use defaultdict :(
                types[model_class] += 1
                model_class.objects.get_or_create(
                    text_ng=obj,
                    label=label,
                    defaults=initial_field_values
                )

            for model_class in types.keys():
                inline = self.get_inline_for_model(model_class)
                inline.max_num = types[model_class]
                inline_instance = inline(self.model, self.admin_site)
                inline_instances.append(inline_instance)
        return inline_instances

    def render(self, context, instance, placeholder):
        context = super(TextPluginNextGeneration, self).render(context, instance, placeholder)
        template = get_template(instance.template.path)
        variables = get_variables_from_template(template)

        for label, variable in variables.items():
            model_class = variable['type']
            initial_field_values = variable['initial_field_values']
            instance_context_name = '%s_instance'% label
            model_queryset = model_class.objects.select_related(*model_class.select_related)
            var = model_queryset.get_or_create(
                text_ng=instance,
                label=label,
                defaults=initial_field_values
            )[0]
            context[label] = var.value
            context[instance_context_name] = var
        context.update({'body': mark_safe(template.render(context))})
        return context


plugin_pool.register_plugin(TextPluginNextGeneration)
