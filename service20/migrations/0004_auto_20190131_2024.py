# Generated by Django 2.1.5 on 2019-01-31 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0003_auto_20190131_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ms_apl',
            name='apl_id',
            field=models.CharField(max_length=10, verbose_name='지원자ID(학번)'),
        ),
    ]
