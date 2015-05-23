# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('act_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_comments',
            name='act',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table_comments',
            name='user',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table_likes',
            name='act',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table_likes',
            name='user',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table_pages',
            name='act',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='table_pages',
            name='user',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
