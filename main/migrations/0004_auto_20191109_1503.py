# Generated by Django 2.2.6 on 2019-11-09 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_account_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production',
            name='prod_img',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='prod_price',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='tk_service',
            field=models.BooleanField(default=False),
        ),
    ]
