# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-09 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('organisation_name', models.CharField(max_length=254, verbose_name='Who you are')),
                ('strapline', models.CharField(max_length=254, verbose_name='Organisation strap line')),
                ('copyright_notice', models.CharField(blank=True, max_length=526, null=True, verbose_name='Copyright notice to appear on footer pages')),
                ('featured_page_1', models.ForeignKey(blank=True, help_text='Choose an awesome page to feature.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='First featured page')),
                ('featured_page_2', models.ForeignKey(blank=True, help_text='Choose another awesome page.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Second featured page')),
                ('featured_page_3', models.ForeignKey(blank=True, help_text='You should probably add a third page too.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Third featured page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
