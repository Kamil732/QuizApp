# Generated by Django 3.0.4 on 2020-04-11 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0013_auto_20200411_2312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='show_points',
            new_name='show_time',
        ),
    ]
