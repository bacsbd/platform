# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-01 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_userpasswordchange'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpasswordchange',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPasswordChange',
        ),
    ]
