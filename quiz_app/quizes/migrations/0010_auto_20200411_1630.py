# Generated by Django 3.0.4 on 2020-04-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0009_auto_20200410_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='is_published',
            field=models.CharField(choices=[('True', 'Publish'), ('False', 'Private')], default='True', max_length=5),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='show_fb_and_web',
            field=models.CharField(choices=[('True', 'Yes'), ('False', 'No')], default='False', max_length=5),
        ),
    ]