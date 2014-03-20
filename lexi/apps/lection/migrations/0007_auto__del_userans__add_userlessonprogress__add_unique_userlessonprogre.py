# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserAns'
        db.delete_table(u'lection_userans')

        # Adding model 'UserLessonProgress'
        db.create_table(u'lection_userlessonprogress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='progress', to=orm['users.User'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(related_name='progress', to=orm['lection.Lesson'])),
            ('units', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=255)),
        ))
        db.send_create_signal(u'lection', ['UserLessonProgress'])

        # Adding unique constraint on 'UserLessonProgress', fields ['user', 'lesson']
        db.create_unique(u'lection_userlessonprogress', ['user_id', 'lesson_id'])

        # Deleting field 'Question.course'
        db.delete_column(u'lection_question', 'course_id')

        # Deleting field 'Question.lesson'
        db.delete_column(u'lection_question', 'lesson_id')


    def backwards(self, orm):
        # Removing unique constraint on 'UserLessonProgress', fields ['user', 'lesson']
        db.delete_unique(u'lection_userlessonprogress', ['user_id', 'lesson_id'])

        # Adding model 'UserAns'
        db.create_table(u'lection_userans', (
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Course'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('lesson', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Lesson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Unit'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Question'])),
            ('is_right', self.gf('django.db.models.fields.BooleanField')()),
            ('is_last', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Answer'])),
            ('time_answered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'lection', ['UserAns'])

        # Deleting model 'UserLessonProgress'
        db.delete_table(u'lection_userlessonprogress')


        # User chose to not deal with backwards NULL issues for 'Question.course'
        raise RuntimeError("Cannot reverse this migration. 'Question.course' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.course'
        db.add_column(u'lection_question', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Course']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Question.lesson'
        raise RuntimeError("Cannot reverse this migration. 'Question.lesson' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.lesson'
        db.add_column(u'lection_question', 'lesson',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lection.Lesson']),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lection.answer': {
            'Meta': {'object_name': 'Answer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_right': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['lection.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'lection.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lection.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lessons'", 'to': u"orm['lection.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lection.question': {
            'Meta': {'object_name': 'Question'},
            'after_video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['lection.Unit']"})
        },
        u'lection.unit': {
            'Meta': {'object_name': 'Unit'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'units'", 'to': u"orm['lection.Lesson']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200'})
        },
        u'lection.userlessonprogress': {
            'Meta': {'unique_together': "(('user', 'lesson'),)", 'object_name': 'UserLessonProgress'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'progress'", 'to': u"orm['lection.Lesson']"}),
            'units': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'progress'", 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_teacher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'userpic': ('core.utils.thumbs.ImageWithThumbsField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['lection']