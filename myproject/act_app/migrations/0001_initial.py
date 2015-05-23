# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table_Activity_Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('act_title', models.TextField()),
                ('event_type', models.TextField()),
                ('price', models.TextField()),
                ('date', models.DateTimeField()),
                ('time', models.DateTimeField()),
                ('duration_days', models.IntegerField()),
                ('is_long_term', models.TextField()),
                ('url', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table_Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('comment', models.TextField()),
                ('act', models.ForeignKey(to='act_app.Table_Activity_Data')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table_Likes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('act', models.ForeignKey(to='act_app.Table_Activity_Data')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table_Pages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('selection_date', models.DateTimeField()),
                ('act', models.ForeignKey(to='act_app.Table_Activity_Data')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table_User_Data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_title', models.TextField()),
                ('user', models.CharField(max_length=32)),
                ('date', models.DateTimeField()),
                ('FCBanner', models.TextField(default=b'#394E06')),
                ('BCBanner', models.TextField(default=b'green')),
                ('FSBanner', models.TextField(default=b'20px')),
                ('FCMenu', models.TextField(default=b'#fff')),
                ('BCMenu', models.TextField(default=b'#7fa71f')),
                ('FSMenu', models.TextField(default=b'12px')),
                ('FCLog', models.TextField(default=b'#999999')),
                ('BCLog', models.TextField(default=b'#FFF')),
                ('FSLog', models.TextField(default=b'11px')),
                ('FCPie', models.TextField(default=b'#484848')),
                ('BCPie', models.TextField(default=b'#f4f4f4')),
                ('FSPie', models.TextField(default=b'10px')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='table_pages',
            name='user',
            field=models.ForeignKey(to='act_app.Table_User_Data'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='table_likes',
            name='user',
            field=models.ForeignKey(to='act_app.Table_User_Data'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='table_comments',
            name='user',
            field=models.ForeignKey(to='act_app.Table_User_Data'),
            preserve_default=True,
        ),
    ]
