# Generated by Django 5.0.3 on 2024-03-31 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_alter_profile_picture_alter_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='privacy',
            field=models.BooleanField(blank=True, default=0),
        ),
    ]
