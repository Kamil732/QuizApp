# Generated by Django 3.0.4 on 2020-04-02 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0002_auto_20200402_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizopinion',
            name='content',
            field=models.TextField(max_length=10000),
        ),
    ]
