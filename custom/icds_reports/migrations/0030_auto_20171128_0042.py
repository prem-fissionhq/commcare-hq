# Generated by Django 1.11.7 on 2017-11-28 00:42

from django.db import migrations

from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0029_add_add_and_dob_to_intermediate_tables'),
    ]

    operations = [
        migrator.get_migration('update_tables14.sql'),
    ]
