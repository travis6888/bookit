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
            ('start_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('picture', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('event_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('start_dateTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_dateTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Event'])

        # Adding model 'Profile'
        db.create_table(u'quick_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile', null=True, to=orm['auth.User'])),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('business', self.gf('django.db.models.fields.BooleanField')(default=False)),
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

        # Adding model 'FreeTimes'
        db.create_table(u'quick_freetimes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('free_time_start', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('free_time_end', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('free_time_amount', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('previous_event', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('free_start_dateTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('free_end_dateTime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['FreeTimes'])

        # Adding model 'Friend'
        db.create_table(u'quick_friend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=6000, null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Friend'])

        # Adding model 'Interest'
        db.create_table(u'quick_interest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interests', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'quick', ['Interest'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'quick_event')

        # Deleting model 'Profile'
        db.delete_table(u'quick_profile')

        # Removing M2M table for field interests on 'Profile'
        db.delete_table(db.shorten_name(u'quick_profile_interests'))

        # Deleting model 'FreeTimes'
        db.delete_table(u'quick_freetimes')

        # Deleting model 'Friend'
        db.delete_table(u'quick_friend')

        # Deleting model 'Interest'
        db.delete_table(u'quick_interest')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'quick.event': {
            'Meta': {'object_name': 'Event'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '8000', 'null': 'True', 'blank': 'True'}),
            'end_dateTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'start_dateTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'quick.freetimes': {
            'Meta': {'object_name': 'FreeTimes'},
            'free_end_dateTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'free_start_dateTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'free_time_amount': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'free_time_end': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'free_time_start': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_event': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'quick.friend': {
            'Meta': {'object_name': 'Friend'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '6000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'quick.interest': {
            'Meta': {'object_name': 'Interest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'quick.profile': {
            'Meta': {'object_name': 'Profile'},
            'business': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['quick.Interest']", 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['quick']