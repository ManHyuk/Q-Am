# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(default=None, max_length=32, unique=True),
        ),
    ]
