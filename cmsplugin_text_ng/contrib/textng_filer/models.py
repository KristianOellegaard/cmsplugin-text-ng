# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from cmsplugin_text_ng.models import TextNGVariableBase
from cmsplugin_text_ng.type_registry import register_type

class TextNGVariableFilerImage(TextNGVariableBase):
    value = FilerImageField(null=True, blank=True, verbose_name=_('value'))

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

register_type('image', TextNGVariableFilerImage)