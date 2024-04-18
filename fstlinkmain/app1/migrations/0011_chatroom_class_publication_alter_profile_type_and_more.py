# Generated by Django 5.0.3 on 2024-03-30 15:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_remove_profile_email_remove_profile_nom_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Class_publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('attachement', models.FileField(null=True, upload_to='classroom_files/')),
                ('date_pub', models.DateTimeField(auto_now_add=True)),
                ('type', models.TextField(choices=[('devoir', 'devoir'), ('annonce', 'annonce')], null=True)),
                ('note', models.IntegerField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.TextField(choices=[('Etudiant', 'Etudiant'), ('Enseignant', 'Enseignant'), ('Entreprise', 'Entreprise')], null=True),
        ),
        migrations.CreateModel(
            name='Class_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.class_publication')),
            ],
        ),
        migrations.CreateModel(
            name='Class_rendu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('attachement', models.FileField(null=True, upload_to='classroom_files/')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.class_publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.enseignant')),
            ],
        ),
        migrations.CreateModel(
            name='Classe_etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.etudiant')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.classroom')),
            ],
        ),
        migrations.AddField(
            model_name='class_publication',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.classroom'),
        ),
        migrations.CreateModel(
            name='Connetion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateConnection', models.DateField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Diplome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('etablissement', models.CharField(max_length=50)),
                ('mention', models.CharField(max_length=50)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_msg', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.chatroom')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('media', models.ImageField(upload_to='post_imgs/')),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.publication')),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('level', models.TextField(choices=[('Débutant', 'Débutant'), ('intermédiaire', 'intermédiaire'), ('avancée', 'avancée'), ('expert', 'expert')], null=True)),
                ('type', models.TextField(choices=[('skill', 'skill'), ('langue', 'langue')], null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
