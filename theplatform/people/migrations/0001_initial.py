# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-06-09 20:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('introduction', models.TextField(blank=True, help_text='Text to describe the index page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PersonLocationRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PersonPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='pilcrow', template='blocks/paragraph.html')), ('header', wagtail.wagtailcore.blocks.StructBlock((('header_text', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='Header', required=False)), ('size', wagtail.wagtailcore.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))), classname='title', icon='title', template='blocks/header.html')), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.CharBlock(blank=True, required=False)), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('', 'Select an image size'), ('full', 'Full-width'), ('contain', 'Contained-width'), ('half', 'Half-width')], required=False))), icon='image', template='blocks/image.html')), ('blockquote', wagtail.wagtailcore.blocks.StructBlock((('text', wagtail.wagtailcore.blocks.TextBlock()), ('attribute_name', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='e.g. Guy Picciotto', required=False)), ('attribute_group', wagtail.wagtailcore.blocks.CharBlock(blank=True, label='e.g. Fugazi', required=False))), icon='openquote', template='blocks/blockquote.html')), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks'))), blank=True, verbose_name="Person's biography")),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PersonSkillsRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('person_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_skills_relationship', to='people.PersonPage')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='PersonStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='PersonStatusRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='person_status_relationship', to='people.PersonPage')),
                ('person_statuses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_person_relationship', to='people.PersonStatus')),
            ],
        ),
    ]