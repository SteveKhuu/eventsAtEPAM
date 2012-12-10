# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Events'
        db.create_table('eventsAtEPAM_events', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('eventsAtEPAM', ['Events'])


    def backwards(self, orm):
        # Deleting model 'Events'
        db.delete_table('eventsAtEPAM_events')


    models = {
        'eventsAtEPAM.events': {
            'Meta': {'object_name': 'Events'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['eventsAtEPAM']