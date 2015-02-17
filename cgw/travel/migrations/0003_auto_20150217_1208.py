# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_auto_20150217_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='group_id',
            field=models.ForeignKey(default=0, to='travel.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quote',
            name='group_id',
            field=models.ForeignKey(default=0, to='travel.Group'),
            preserve_default=False,
        ),
    ]
