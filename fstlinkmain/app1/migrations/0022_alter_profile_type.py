# Generated by Django 5.0.3 on 2024-03-31 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_alter_profile_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.TextField(blank=True, choices=[('Etudiant', 'Etudiant'), ('Enseignant', 'Enseignant'), ('Entreprise', 'Entreprise')], null=True),
        ),
    ]
