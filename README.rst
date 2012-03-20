cmsplugin-text-ng
=================

An enhanced version of the ``Text`` plugin for `django CMS`_. It allows wrapping
the text plugin inside a template selectable by the CMS content editor.

.. note::
    This plugin is not meant to replace ``cms.plugins.text``. It is an
    enhancement for certain use cases. For most types of content, you should
    probably still use ``cms.plugins.text`` or write a specifically tailored
    plugin.

Installation
============

 * Add ``cmsplugin_text_ng`` to your ``INSTALLED_APPS``.
 * Create some templates (more on that soon) and add them in the admin.


Basic example: static template
------------------------------

Let's say you want to have a text plugin with a facebook "like" button. Your
template could look something like this::

    <div class="text left">
        {{ body|safe }}
    </div>
    <div class="fb-like right">
        <h2>Like this page on facebook!</h2>
        <fb:like send="false" width="450" show_faces="true"></fb:like>
    </div>


Advanced example: dynamic template
----------------------------------

Let's assume you want to set the content of the ``<h2>``-tag on a per-plugin
basis. No problem! That's what the ``{% define %}`` template tag does::

    {% load text_ng_tags %}
    {% define h2_content as text %}
    <div class="text left">
        {{ body|safe }}
    </div>
    <div class="fb-like right">
        <h2>{{ h2_content }}</h2>
        <fb:like send="false" width="450" show_faces="true"></fb:like>
    </div>

When you edit the plugin, you will now have a text box with the "h2_content" as
a label. Its content will be added to the context when rendering the plugin. You
can access it like any context variable: ``{{ h2_content }}``.

The ``as text`` part of the template tag refers to the type of the variable.
cmsplugin-text-ng comes with one type (``text``). Additionally, there is an
``image`` type in ``cmsplugin_text_ng.contrib.textng_filer`` that uses
`django-filer`_ to add images to the template context. If you want to use it,
make sure that both ``filer`` and ``cmsplugin_text_ng.contrib.textng_file`` are
listed in your ``INSTALLED_APPS``.

Really (just kidding) advanced example: define your own types
-------------------------------------------------------------

So, you want to add some HTML code right below the "like" button, and your
content editors insist on using TinyMCE. Let's do this! Using the awesome
``HTMLField`` from `django-tinymce`_, we set up a model with a tinymce'd
textarea::

    from django.utils.translation import ugettext_lazy as _

    from tinymce.models import HTMLField

    from cmsplugin_text_ng.models import TextNGVariableBase
    from cmsplugin_text_ng.type_registry import register_type

    class TextNGVariableHTML(TextNGVariableBase):
        value = HTMLField(null=True, verbose_name=_('value'))

        class Meta:
            verbose_name = _('html text')
            verbose_name_plural = _('html texts')

    register_type('htmltext', TextNGVariableHTML)

A couple of things to note:

 * your type has to inherit from ``TextNGVariableBase``.
 * the field containing the data that should end up in the context has to be
   named "value"
 * it has to be nullable (the ``null=True`` part).
 * the type name (``htmltext`` in the example) has to be unique over the whole
   project. You might want to prefix it with something unique to your app.

cmsplugin-text-ng will complain (loudly!) if these conditions are not met.

Where were we? Right, the template. To use your new, awesome type in a template,
just use the ``{% define %}`` tag to your advantage, like so::

    {% load text_ng_tags %}
    {% define h2_content as text %}
    {% define html_content as htmltext %}
    <div class="text left">
        {{ body|safe }}
    </div>
    <div class="fb-like right">
        <h2>{{ h2_content }}</h2>
        <fb:like send="false" width="450" show_faces="true"></fb:like>
        {{ html_content|safe }}
    </div>

Done.

.. _django CMS: https://www.django-cms.org
.. _django-filer: https://github.com/stefanfoulis/django-filer
.. _django-tinymce: https://github.com/aljosa/django-tinymce