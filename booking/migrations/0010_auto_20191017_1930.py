# Generated by Django 2.2.3 on 2019-10-17 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_bklist_is_comfirm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bklist',
            old_name='is_comfirm',
            new_name='is_confirm',
        ),
    ]