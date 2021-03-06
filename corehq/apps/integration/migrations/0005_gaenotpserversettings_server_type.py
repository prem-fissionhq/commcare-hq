# Generated by Django 2.2.16 on 2020-10-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('integration', '0004_gaenotpserversettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='gaenotpserversettings',
            name='server_type',
            field=models.CharField(choices=[('NEARFORM', 'NearForm OTP Server'),
                                            ('APHL', 'APHL Exposure Notifications')],
                                   default='NEARFORM', max_length=255),
        ),
    ]
