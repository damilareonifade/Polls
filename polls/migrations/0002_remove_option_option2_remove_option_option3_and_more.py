# Generated by Django 4.0.6 on 2022-07-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='option2',
        ),
        migrations.RemoveField(
            model_name='option',
            name='option3',
        ),
        migrations.AlterField(
            model_name='option',
            name='option_count',
            field=models.BigIntegerField(),
        ),
    ]
