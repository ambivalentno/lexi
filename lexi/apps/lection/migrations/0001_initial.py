# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'lection_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal(u'lection', ['Course'])

        # Adding model 'Lesson'
        db.create_table(u'lection_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Course'])),
        ))
        db.send_create_signal(u'lection', ['Lesson'])

        # Adding model 'Unit'
        db.create_table(u'lection_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('explanation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('video', self.gf('embed_video.fields.EmbedVideoField')(max_length=200)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Lesson'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'lection', ['Unit'])

        # Adding model 'Question'
        db.create_table(u'lection_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('after_video', self.gf('embed_video.fields.EmbedVideoField')(max_length=200, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Unit'], null=True)),
        ))
        db.send_create_signal(u'lection', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'lection_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_right', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Question'])),
        ))
        db.send_create_signal(u'lection', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'lection_course')

        # Deleting model 'Lesson'
        db.delete_table(u'lection_lesson')

        # Deleting model 'Unit'
        db.delete_table(u'lection_unit')

        # Deleting model 'Question'
        db.delete_table(u'lection_question')

        # Deleting model 'Answer'
        db.delete_table(u'lection_answer')


    models = {
        u'lection.answer': {
            'Meta': {'object_name': 'Answer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_right': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lection.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'lection.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lection.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lection.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lection.question': {
            'Meta': {'object_name': 'Question'},
            'after_video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lection.Unit']", 'null': 'True'})
        },
        u'lection.unit': {
            'Meta': {'object_name': 'Unit'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lection.Lesson']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['lection']