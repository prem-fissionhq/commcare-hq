# Generated by Django 2.2.13 on 2020-09-04 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_hqapikey_role_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hqapikey',
            name='domain',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]