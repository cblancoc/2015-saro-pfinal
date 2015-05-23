# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('act_app', '0005_table_user_data_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table_user_data',
            old_name='BCPie',
            new_name='BCFooter',
        ),
        migrations.RenameField(
            model_name='table_user_data',
            old_name='BCLog',
            new_name='BCLogin',
        ),
        migrations.RenameField(
            model_name='table_user_data',
            old_name='FCPie',
            new_name='FCFooter',
        ),
        migrations.RenameField(
            model_name='table_user_data',
            old_name='FCLog',
            new_name='FCLogin',
        ),
        migrations.RenameField(
            model_name='table_user_data',
            old_name='FSPie',
            new_name='FSFooter',
        ),
        migrations.RenameField(
            model_name='table_user_data',
            old_name='FSLog',
            new_name='FSLogin',
        ),
        migrations.RemoveField(
            model_name='table_user_data',
            name='BCBanner',
        ),
        migrations.RemoveField(
            model_name='table_user_data',
            name='FCBanner',
        ),
        migrations.RemoveField(
            model_name='table_user_data',
            name='FSBanner',
        ),
    ]
