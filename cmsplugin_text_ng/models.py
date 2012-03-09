from django.db import models
from cms.plugins.text.models import AbstractText
from django.utils.translation import ugettext_lazy as _

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