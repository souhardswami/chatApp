# Generated by Django 3.0.8 on 2020-07-29 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200729_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joincode',
            old_name='user',
            new_name='creater',
        ),
        migrations.AlterField(
            model_name='joincode',
            name='joiner',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
