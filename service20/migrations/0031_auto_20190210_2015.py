# Generated by Django 2.1.5 on 2019-02-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service20', '0030_auto_20190210_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='ms_sub',
            name='att_seq',
            field=models.PositiveIntegerField(blank=True, max_length=1, null=True, verbose_name='속성 SEQ → PK 자동생성 시 필요없음'),
        ),
        migrations.AlterField(
            model_name='ms_sub',
            name='att_cdd',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='속성 CODE'),
        ),
        migrations.AlterUniqueTogether(
            name='ms_sub',
            unique_together={('ms_id', 'att_id', 'att_seq')},
        ),
    ]
