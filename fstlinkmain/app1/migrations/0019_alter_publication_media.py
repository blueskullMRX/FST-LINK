# Generated by Django 5.0.3 on 2024-03-31 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_alter_publication_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='media',
            field=models.ImageField(blank=True, null=True, upload_to='post_imgs/'),
        ),
    ]
