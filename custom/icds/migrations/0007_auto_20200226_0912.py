# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-02-26 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icds', '0006_hostedccz_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostedCCZCustomSupportingFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='hostedcczsupportingfile',
            name='display',
            field=models.IntegerField(choices=[(1, 'list'), (2, 'footer'), (3, 'custom')]),
        ),
        migrations.AddField(
            model_name='hostedcczcustomsupportingfile',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icds.HostedCCZSupportingFile'),
        ),
        migrations.AddField(
            model_name='hostedcczcustomsupportingfile',
            name='link',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='icds.HostedCCZLink'),
        ),
    ]
