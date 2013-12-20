from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

if 'djangocms_text_ckeditor' in settings.INSTALLED_APPS:
    from djangocms_text_ckeditor.models import AbstractText
    from djangocms_text_ckeditor.cms_plugins import TextPlugin
else:
    try:
        from cms.plugins.text.models import AbstractText
        from cms.plugins.text.cms_plugins import TextPlugin
    except ImportError:
        raise ImproperlyConfigured('For django-cms >= 3 you need to install djangocms-text-ckeditor')
