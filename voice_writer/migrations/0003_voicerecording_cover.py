# Generated by Django 5.0.7 on 2024-08-20 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice_writer', '0002_alter_voicerecording_bitrate_kbps_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voicerecording',
            name='cover',
            field=models.FileField(blank=True, upload_to='user_uploads/voice'),
        ),
    ]
