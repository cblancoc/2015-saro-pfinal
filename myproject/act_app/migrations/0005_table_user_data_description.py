# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('act_app', '0004_auto_20150516_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='table_user_data',
            name='description',
            field=models.TextField(default=()),
            preserve_default=False,
        ),
    ]
