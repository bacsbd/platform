# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-06-25 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170625_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]
