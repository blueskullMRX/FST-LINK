# Generated by Django 5.0.3 on 2024-04-01 00:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_alter_diplome_nom'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='date_msg',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='name',
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chatroom',
            name='user2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classroom',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='title',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='diplome',
            name='etablissement',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='etablissement',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='nom',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projet',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='projet',
            name='nom',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='nom',
            field=models.TextField(),
        ),
    ]
