# Generated by Django 2.1.5 on 2019-02-12 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0035_auto_20190212_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='com_cdd',
            name='std_grp_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service20.com_cdh', verbose_name='그룹코드'),
        ),
    ]
