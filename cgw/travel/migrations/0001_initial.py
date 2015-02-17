# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('inCarrier', models.CharField(max_length=30)),
                ('outCarrier', models.CharField(max_length=30)),
                ('depDate', models.DateTimeField(verbose_name='departure date')),
                ('retDate', models.DateTimeField(verbose_name='return date')),
                ('direct', models.BooleanField(default=False)),
                ('origin', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=30)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
