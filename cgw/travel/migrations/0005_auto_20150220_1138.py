# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_auto_20150217_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('carrier', models.CharField(max_length=30, default='')),
                ('outgoing', models.BooleanField(default=False)),
                ('quote_id', models.ForeignKey(to='travel.Quote')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='quote',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='in_carrier',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='quote',
            name='out_carrier',
        ),
        migrations.AddField(
            model_name='quote',
            name='in_destination',
            field=models.CharField(max_length=30, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quote',
            name='in_origin',
            field=models.CharField(max_length=30, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quote',
            name='out_destination',
            field=models.CharField(max_length=30, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quote',
            name='out_origin',
            field=models.CharField(max_length=30, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=50, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=50, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quote',
            name='dep_date',
            field=models.DateTimeField(null=True, verbose_name='departure date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quote',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quote',
            name='ret_date',
            field=models.DateTimeField(null=True, verbose_name='return date'),
            preserve_default=True,
        ),
    ]
