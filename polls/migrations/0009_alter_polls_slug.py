# Generated by Django 4.0.6 on 2022-07-29 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_alter_polls_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polls',
            name='slug',
            field=models.CharField(blank=True, help_text='Required', max_length=255, null=True),
        ),
    ]
