# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TextNGTemplateCategory'
        db.create_table('cmsplugin_text_ng_textngtemplatecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('cmsplugin_text_ng', ['TextNGTemplateCategory'])

        # Adding model 'TextNGTemplate'
        db.create_table('cmsplugin_text_ng_textngtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsplugin_text_ng.TextNGTemplateCategory'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('cmsplugin_text_ng', ['TextNGTemplate'])

        # Adding model 'TextNG'
        db.create_table('cmsplugin_textng', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmsplugin_text_ng.TextNGTemplate'])),
        ))
        db.send_create_signal('cmsplugin_text_ng', ['TextNG'])


    def backwards(self, orm):
        
        # Deleting model 'TextNGTemplateCategory'
        db.delete_table('cmsplugin_text_ng_textngtemplatecategory')

        # Deleting model 'TextNGTemplate'
        db.delete_table('cmsplugin_text_ng_textngtemplate')

        # Deleting model 'TextNG'
        db.delete_table('cmsplugin_textng')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'cmsplugin_text_ng.textng': {
            'Meta': {'object_name': 'TextNG', 'db_table': "'cmsplugin_textng'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmsplugin_text_ng.TextNGTemplate']"})
        },
        'cmsplugin_text_ng.textngtemplate': {
            'Meta': {'ordering': "['title']", 'object_name': 'TextNGTemplate'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmsplugin_text_ng.TextNGTemplateCategory']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'cmsplugin_text_ng.textngtemplatecategory': {
            'Meta': {'ordering': "['title']", 'object_name': 'TextNGTemplateCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['cmsplugin_text_ng']
