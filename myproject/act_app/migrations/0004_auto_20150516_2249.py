# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('act_app', '0003_table_last_refresh'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table_Selected_Acts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('act', models.IntegerField()),
                ('user', models.TextField()),
                ('selection_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Table_Pages',
        ),
    ]
