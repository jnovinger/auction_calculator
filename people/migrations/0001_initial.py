# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [(b'people', '0001_initial'), (b'people', '0002_auto_20151108_2006'), (b'people', '0003_auto_20151108_2114'), (b'people', '0004_auto_20151108_2119')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lahmanID', models.CharField(help_text='ID used in Lahman Database version 4.0', unique=True, max_length=10, db_index=True, blank=True)),
                ('lahman40ID', models.CharField(help_text='ID used in Lahman Database version 4.0', unique=True, max_length=10, db_index=True, blank=True)),
                ('lahman45ID', models.CharField(help_text='ID used in Lahman database version 4.5', unique=True, max_length=10, db_index=True, blank=True)),
                ('retroID', models.CharField(help_text='ID used by retrosheet', unique=True, max_length=10, db_index=True, blank=True)),
                ('holtzID', models.CharField(help_text="ID used by Sean Holtz's Baseball Almanac", unique=True, max_length=10, db_index=True, blank=True)),
                ('bbrefID', models.CharField(help_text='ID used by Baseball Reference website', unique=True, max_length=10, db_index=True, blank=True)),
                ('mlbamID', models.CharField(help_text='ID used by MLB Advanced Media', unique=True, max_length=10, db_index=True, blank=True)),
                ('birth', models.DateField(null=True, blank=True)),
                ('death', models.DateField(null=True, blank=True)),
                ('given_name', models.CharField(max_length=255, blank=True)),
                ('family_name', models.CharField(max_length=255, blank=True)),
                ('debut', models.DateField(null=True, blank=True)),
                ('final_game', models.DateField(null=True, blank=True)),
                ('birth_city', models.CharField(max_length=255, blank=True)),
                ('birth_country', models.CharField(max_length=255, blank=True)),
                ('birth_state', models.CharField(max_length=255, blank=True)),
                ('death_city', models.CharField(max_length=255, blank=True)),
                ('death_country', models.CharField(max_length=255, blank=True)),
                ('death_state', models.CharField(max_length=255, blank=True)),
            ],
        ),
    ]
