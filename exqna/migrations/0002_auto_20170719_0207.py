# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-18 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exqna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraquestion',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
