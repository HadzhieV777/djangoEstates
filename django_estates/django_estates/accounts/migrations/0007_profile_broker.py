# Generated by Django 4.0.3 on 2022-04-03 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='broker',
            field=models.BooleanField(default=False),
        ),
    ]
