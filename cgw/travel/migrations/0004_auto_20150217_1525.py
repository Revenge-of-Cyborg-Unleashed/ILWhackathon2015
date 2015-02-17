# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_auto_20150217_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='passengers',
        ),
        migrations.AddField(
            model_name='group',
            name='salt',
            field=models.CharField(max_length=50, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='decided',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quote',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=50, default=''),
            preserve_default=True,
        ),
    ]
