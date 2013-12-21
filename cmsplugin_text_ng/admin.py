from django.contrib import admin

from cmsplugin_text_ng.models import TextNGTemplate, TextNGTemplateCategory


class TextNGTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'path')
    list_filter = ('category',)
    search_fields = ('title', 'category', 'path')

admin.site.register(TextNGTemplate, TextNGTemplateAdmin)

admin.site.register(TextNGTemplateCategory)
