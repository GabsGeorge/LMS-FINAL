# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 17:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curso',
            options={'ordering': ['nome'], 'verbose_name': 'Curso', 'verbose_name_plural': 'Cursos'},
        ),
    ]
