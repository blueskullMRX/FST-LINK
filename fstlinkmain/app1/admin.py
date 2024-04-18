from django.contrib import admin

# Register your models here.

from .models import Profile,Entreprise,Etudiant,Enseignant,Classroom,Classe_etudiant,Diplome,Experience,Projet,Publication,Commentaire,Connetion,ChatRoom,Message,Skills,Class_publication,Class_comments,Class_rendu
admin.site.register((Profile,Entreprise,Etudiant,Enseignant,Classroom,Classe_etudiant,Diplome,Experience,Projet,Publication,Commentaire,Connetion,ChatRoom,Message,Skills,Class_publication,Class_comments,Class_rendu))