# Generated by Django 3.0.4 on 2020-04-01 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='images/default.jpg', upload_to='image'),
        ),
    ]
