from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.plugins.text.models import AbstractText

from cmsplugin_text_ng.type_registry import register_type

class TextNGTemplateCategory(models.Model):
    title = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('template category')
        verbose_name_plural = _('template categories')
        ordering = ['title']


class TextNGTemplate(models.Model):
    category = models.ForeignKey(TextNGTemplateCategory, blank=True, null=True)
    title = models.CharField(max_length=128)
    path = models.CharField(max_length=128)

    def __unicode__(self):
        if self.category:
            return u"%s (%s)" % (self.title, self.category)
        return self.title

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        ordering = ['title']


class TextNG(AbstractText):
    template = models.ForeignKey(TextNGTemplate)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')


class TextNGVariableBase(models.Model):
    select_related = []
    text_ng = models.ForeignKey(TextNG, related_name='+')
    label = models.CharField(_('label'), max_length=20, validators=[RegexValidator(regex='[_a-z]+', message=_('Only lower case characters.'))])

    class Meta:
        abstract = True
        unique_together = ('text_ng', 'label')


class TextNGVariableText(TextNGVariableBase):
    value = models.TextField(_('value'), null=True, blank=True)

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('texts')

register_type('text', TextNGVariableText)