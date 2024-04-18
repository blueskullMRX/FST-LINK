from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Entreprise(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE)

    domaine = models.TextField(max_length=50,null=True)

    def __str__(self):
        return self.user.username

class Etudiant(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE)

    CNE = models.TextField(max_length=10,null=True,unique=True)
    Filiere = models.TextField(null=True)
    en_cherche_stage = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

class Enseignant(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE)

    departement = models.TextField(null=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE)


    birth_date = models.DateField(null=True, blank=True)
    class Type(models.TextChoices):
        etudiant = 'Etudiant', 'Etudiant'
        enseignant = 'Enseignant' , 'Enseignant'
        entreprise = 'Entreprise' , 'Entreprise'

    type = models.TextField(choices=Type.choices ,null=True,blank=True)
    picture = models.ImageField(blank=True,null=True,upload_to="profile_imgs/",default="profile_imgs/default.jpg")
    bio = models.TextField(max_length=500, blank=True,null=True,default="vide bio")
    phonenumber = models.TextField(max_length=14,blank=True,null=True,default="+212000000")
    adresse = models.TextField(blank=True,null=True,default="vide adresse")    
    privacy = models.BooleanField(blank=True,default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    if instance.type == "Entreprise" :
        if not Entreprise.objects.filter(user=instance.user).exists():
            Entreprise.objects.create(user=instance.user)
        if Etudiant.objects.filter(user=instance.user).exists() :
            Etudiant.objects.filter(user=instance.user).delete()
        if Enseignant.objects.filter(user=instance.user).exists() :
            Enseignant.objects.filter(user=instance.user).delete()
    elif instance.type == "Etudiant" :
        if not Etudiant.objects.filter(user=instance.user).exists():
            Etudiant.objects.create(user=instance.user)
        if Entreprise.objects.filter(user=instance.user).exists() :
            Entreprise.objects.filter(user=instance.user).delete()
        if Enseignant.objects.filter(user=instance.user).exists() :
            Enseignant.objects.filter(user=instance.user).delete()
    elif instance.type == "Enseignant" :
        if not Enseignant.objects.filter(user=instance.user).exists():
            Enseignant.objects.create(user=instance.user)
        if Etudiant.objects.filter(user=instance.user).exists() :
            Etudiant.objects.filter(user=instance.user).delete()
        if Entreprise.objects.filter(user=instance.user).exists() :
            Entreprise.objects.filter(user=instance.user).delete()


class Classroom(models.Model):
    title = models.TextField(null=True)
    description= models.TextField(null=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Classe_etudiant(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)


class Diplome(models.Model):
    nom = models.TextField(null=True)
    etablissement = models.TextField(null=True)

    class Mention(models.TextChoices):
        passable = 'Passable', 'Passable'
        assezbien = 'Assez-Bien' , 'Assez_bien'
        bien = 'Bien' , 'Bien'
        tresbien = "Trés-Bien", "Trés-Bien"

    mention = models.TextField(choices=Mention.choices,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start=models.IntegerField(null=True)
    end=models.IntegerField(null=True)
    def __str__(self):
        return self.nom
    
class Experience(models.Model):
    nom = models.TextField(null=True)
    etablissement = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start=models.IntegerField(null=True)
    period=models.IntegerField(null=True)
    def __str__(self):
        return self.nom

class Projet(models.Model):
    nom = models.TextField(null=True)
    description = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date =models.IntegerField(null=True)
    month =models.TextField(null=True)
    
    def __str__(self):
        return self.nom
    
class Publication(models.Model):
    content = models.TextField()
    media = models.ImageField(upload_to='post_imgs/',null=True,blank=True)
    date = models.DateField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content

class Commentaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub = models.ForeignKey(Publication, on_delete=models.CASCADE)
    content= models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} : {self.content}"
    
class Connetion(models.Model):
    follower = models.ForeignKey(User,related_name = "follower",on_delete=models.CASCADE)
    followed = models.ForeignKey(User,related_name = "followed",on_delete=models.CASCADE)
    dateConnection = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.follower} : {self.followed}"
    
class ChatRoom(models.Model):
    user1 = models.ForeignKey(User,related_name = "user1" , on_delete=models.CASCADE)
    user2 = models.ForeignKey(User,related_name = "user2" , on_delete=models.CASCADE)
    counter = models.IntegerField(null=True,default=0)

    def __str__(self):
        return f"{self.user1}:{self.user2}"
    
@receiver(post_save, sender=Connetion)
def create_Connection_room(sender, instance, created, **kwargs):
    if created:
        if  not ChatRoom.objects.filter(user1=instance.follower,user2=instance.followed).exists() and not ChatRoom.objects.filter(user1=instance.followed,user2=instance.follower).exists():
            ChatRoom.objects.create(user1=instance.follower,user2=instance.followed)

    
class Message(models.Model):
    date = models.DateField(auto_now_add=True)
    content= models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom,  on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.sender} : {self.content}"


@receiver(post_save, sender=Message)
def update_chatroom_counter(sender, instance, created, **kwargs):
    if created:
        chatroom = instance.room
        period = timezone.now() - timedelta(hours=24)
        chatroom.counter = Message.objects.filter(room=chatroom,date__gte=period).count()
        chatroom.save()


class Skills(models.Model):
    nom = models.TextField()
    class Level(models.TextChoices):
        Debutant = 'Débutant', 'Débutant'
        intermediaire = 'intermédiaire' , 'intermédiaire'
        avancee = 'avancée' , 'avancée'
        expert = 'expert' , 'expert'

    level = models.TextField(choices=Level.choices ,null=True)

    class Type(models.TextChoices):
        skill = 'skill', 'skill'
        langue = 'langue' , 'langue'

    type = models.TextField(choices=Type.choices ,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom
    
class Class_publication(models.Model):
    content=models.TextField(null=True)
    attachement=models.FileField(null=True,upload_to="classroom_files/")
    date_pub=models.DateTimeField(auto_now_add=True)

    class Type(models.TextChoices):
        devoir = 'devoir', 'devoir'
        annonce = 'annonce' , 'annonce'

    type = models.TextField(choices=Type.choices ,null=True)
    note=models.IntegerField(null=True)
    classroom=models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Class_comments(models.Model):
    content=models.TextField(null=True)
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    publication=models.ForeignKey(Class_publication,on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class Class_rendu(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    publication=models.ForeignKey(Class_publication,on_delete=models.CASCADE)
    content=models.TextField(null=True)
    attachement=models.FileField(null=True,upload_to="classroom_files/")

    def __str__(self):
        return self.content