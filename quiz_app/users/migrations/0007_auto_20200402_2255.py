# Generated by Django 3.0.4 on 2020-04-02 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200401_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
