# Generated by Django 5.0.3 on 2024-03-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_imgs'),
        ),
    ]
