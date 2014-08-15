# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'quick_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=8000, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(max_length=100, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Event'])

        # Adding model 'Interest'
        db.create_table(u'quick_interest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interests', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Interest'])

        # Adding model 'Profile'
        db.create_table(u'quick_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Profile'])

        # Adding M2M table for field interests on 'Profile'
        m2m_table_name = db.shorten_name(u'quick_profile_interests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'quick.profile'], null=False)),
            ('interest', models.ForeignKey(orm[u'quick.interest'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'interest_id'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'quick_event')

        # Deleting model 'Interest'
        db.delete_table(u'quick_interest')

        # Deleting model 'Profile'
        db.delete_table(u'quick_profile')

        # Removing M2M table for field interests on 'Profile'
        db.delete_table(db.shorten_name(u'quick_profile_interests'))


    models = {
        u'quick.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'quick.interest': {
            'Meta': {'object_name': 'Interest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'quick.profile': {
            'Meta': {'object_name': 'Profile'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['quick.Interest']", 'null': 'True', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['quick']