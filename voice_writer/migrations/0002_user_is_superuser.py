# Generated by Django 5.0.7 on 2024-08-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice_writer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
