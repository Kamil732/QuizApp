# Generated by Django 3.0.4 on 2020-04-08 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_show_fb_and_web'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='show_fb_and_web',
        ),
    ]
