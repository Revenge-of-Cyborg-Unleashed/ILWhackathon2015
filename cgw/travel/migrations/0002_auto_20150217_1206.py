# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='depDate',
            new_name='dep_date',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='inCarrier',
            new_name='in_carrier',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='outCarrier',
            new_name='out_carrier',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='retDate',
            new_name='ret_date',
        ),
        migrations.AddField(
            model_name='quote',
            name='passengers',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
