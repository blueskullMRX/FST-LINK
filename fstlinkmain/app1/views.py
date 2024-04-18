from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from .models import *


@login_required(login_url = "login")
def dashboardetd(request):
    if request.user.is_authenticated:
        users= User.objects.all()
        etudiants = Etudiant.objects.all()
        entreprises = Entreprise.objects.all()
        classrooms = {}
        if request.user.profile.type == "Etudiant":
            classrooms = Classe_etudiant.objects.filter(etudiant=request.user.etudiant)
        elif request.user.profile.type == "Enseignant":
            classrooms = Classroom.objects.filter(enseignant=request.user.enseignant)
        chatrooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)

    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    print(chatrooms.count)
            
    return render(request, 'etudiant/etudiant.html', {'users': users,"etudiants":etudiants,"classrooms":classrooms,"chatrooms":chatrooms,"entreprises":entreprises})

@login_required(login_url = "login")
def dashboardhome(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            
            if "post_media" in request.FILES and "post_content" in request.POST:
                Publication.objects.create(user=request.user,media=request.FILES["post_media"],content=request.POST["post_content"])
            elif "post_media" in request.FILES :
                Publication.objects.create(user=request.user,content=request.POST["post_content"])
            elif "post_content" in request.POST:
                Publication.objects.create(user=request.user,content=request.POST["post_content"])
            elif "pub_id" in request.POST:
                pubx= Publication.objects.get(id=request.POST["pub_id"])
                Commentaire.objects.create(user=request.user,pub=pubx,content=request.POST["comment"])
            return redirect("dashboardhome")
        publications = reversed(Publication.objects.all())
        comments=Commentaire.objects.all().order_by('-date')
    return render(request, 'layout/home.html', {"publications": publications,"comments":comments})



def search(request):
    if request.method == "POST" and "search" in request.POST:
        if User.objects.filter(username=request.POST.get("search")).exists():
            us = User.objects.get(username=request.POST.get("search"))
        else:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    
    return redirect(f"profile/{us.username}")




def profile(request,username="mon profil"):
            
    if User.objects.filter(username=username).exists():
        us = User.objects.get(username=username)
        if us.profile.privacy and not request.user.is_authenticated:
            return redirect("home")
    elif username == "mon profil" and request.user.is_authenticated:
        us = request.user
    else :
        return redirect("home")
            
    if request.method == "POST" and "is_followed" in request.POST:
        if request.POST.get("is_followed") == "0":
            Connetion.objects.create(follower=request.user,followed=us)
        else :
            Connetion.objects.filter(follower=request.user,followed=us).delete()
            
    skills = Skills.objects.filter(user=us,type="skill")
    langues = Skills.objects.filter(user=us,type="langue")
    deps = Diplome.objects.filter(user=us)
    projects = Projet.objects.filter(user=us)
    experiences = Experience.objects.filter(user=us)

    is_followed = 0
    if request.user.is_authenticated and Connetion.objects.filter(follower=request.user,followed=us).exists():
        is_followed = 1


    return render(request,'layout/profile.html',{"user":us,"skills":skills,"langues":langues,"deps":deps,"projects":projects,"experiences":experiences,"is_followed":is_followed})
    
@login_required(login_url = "login")
def profilesettings(request):
    if request.user.is_authenticated:
        us = request.user
        skills = Skills.objects.filter(user=us,type="skill")
        langues = Skills.objects.filter(user=us,type="langue")
        deps = Diplome.objects.filter(user=us)
        projects = Projet.objects.filter(user=us)
        experiences = Experience.objects.filter(user=us)
    else :
        return redirect("home")
    
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        if "picture" in request.FILES :
            profile.picture = request.FILES.get("picture")
            profile.save()
        elif 'bio' in request.POST:
            profile.bio = request.POST.get("bio")
            profile.save()
        elif 'skill' in request.POST:
            Skills.objects.create(user=request.user ,nom=request.POST.get("skill"),level=request.POST.get("skill_lvl"),type="skill")
        elif "selected_skill" in request.POST:
            selected = Skills.objects.filter(id=request.POST.get("selected_skill"))
            selected.delete()
        elif "langue" in request.POST:
            Skills.objects.create(user=request.user ,nom=request.POST.get("langue"),level=request.POST.get("langue_lvl"),type="langue")
        elif "selected_langue" in request.POST:
            selected = Skills.objects.filter(id=request.POST.get("selected_langue"))
            selected.delete()
        elif "adresse" in request.POST:
            profile.adresse = request.POST.get("adresse")
            profile.save()
        elif "number" in request.POST:
            profile.phonenumber = request.POST.get("number")
            profile.save()
        elif "dep_nom" in request.POST:
            Diplome.objects.create(user=request.user ,nom=request.POST.get("dep_nom"),etablissement=request.POST.get("dep_etab"),mention=request.POST.get("mention"),start=request.POST.get("dep_debut"),end=request.POST.get("dep_fin"))
        elif "selected_dep" in request.POST:
            selected = Diplome.objects.filter(id=request.POST.get("selected_dep"))
            selected.delete()
        elif "projet_titre" in request.POST:
            Projet.objects.create(user=request.user ,nom=request.POST.get("projet_titre"),description=request.POST.get("projet_desc"),date=request.POST.get("projet_annee"),month=request.POST.get("projet_month"))
        elif "selected_projet" in request.POST:
            selected = Projet.objects.filter(id=request.POST.get("selected_projet"))
            selected.delete()
        elif "exp_nom" in request.POST:
            Experience.objects.create(user=request.user ,nom=request.POST.get("exp_nom"),etablissement=request.POST.get("exp_nom"),start=request.POST.get("exp_start"),period=request.POST.get("exp_period"))
        elif "selected_experience" in request.POST:
            selected = Experience.objects.filter(id=request.POST.get("selected_experience"))
            selected.delete()
        elif "privacy" in request.POST:
            value = int(request.POST.get("privacy"))
            profile.privacy = value
            profile.save()

    return render(request,'layout/profilesettings.html',{"skills":skills,"langues":langues,"deps":deps,"projects":projects,"experiences":experiences})


@login_required(login_url = "login")
def chat(request,chatroom_id="none"):
    chatrooms = ChatRoom.objects.filter(user1=request.user) | ChatRoom.objects.filter(user2=request.user)
    if chatroom_id == "none" :
        if len(chatrooms)!=0:
            chatroom_id = chatrooms[0].id
        else :
            return redirect('dashboardetd')
    selected = ChatRoom.objects.get(id=chatroom_id)
    if selected.user1 != request.user and selected.user2 != request.user :
        return redirect("/chat")
    messages = Message.objects.filter(room=selected)

    if request.method == "POST" and "message" in request.POST:
        Message.objects.create(sender=request.user,room=selected,content=request.POST.get("message"))


    return render(request,'layout/chat.html',{"chatrooms":chatrooms,"selected":selected,"messages":messages})

    
def home(request):
    us=User.objects.all()
    profs=Enseignant.objects.all()
    etu=Etudiant.objects.all()
    return render(request,"layout/homegen.html",{'etudiants':etu,'professeurs':profs,'users':us})

def logout(request):
    auth.logout(request)
    return redirect("home")


def login(request):

    if not request.user.is_authenticated :
        username = None
        password = None

        if request.method == "POST" :
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request,username=username,password=password)
            if user is not None :
                auth.login(request,user)
                #return render(request,"layout/chat.html")
                return redirect("home")
        
        context = {"name":username,"pass":password}

        return render(request,"layout/login.html",context)
    else :
        return redirect("home")


def register(request):
    if not request.user.is_authenticated :
        if request.method == "POST":
            username = request.POST.get("username")
            first_name = request.POST.get("first_name")
            domaine = request.POST.get("domaine")
            email=request.POST.get("email")
            phonenumber = request.POST.get("phonenumber")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            if password != password2 :
                return redirect("register")

            User.objects.create(username=username,first_name=first_name,email=email,password=make_password(password))
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            profile.phonenumber = phonenumber
            profile.type="Entreprise"
            profile.save()

            entreprise = Entreprise.objects.get(user=user)
            entreprise.domaine = domaine
            entreprise.save()
            return redirect("login")

        return render(request,"entreprise/register.html")
    else :
        return redirect("home")

@login_required(login_url = "login")
def classrooms(request):
    
    if request.user.is_authenticated:
        us= request.user
        profile = Profile.objects.get(user=us)
        if profile.type == "Etudiant":
            etd=Etudiant.objects.get(user=us)
            classrooms = Classe_etudiant.objects.filter(etudiant=etd)
        elif profile.type == "Enseignant":
            ens=Enseignant.objects.get(user=us)
            classrooms = Classroom.objects.filter(enseignant=ens)
        
    
    return render(request,"etudiant/classrooms.html",{"classrooms":classrooms})

@login_required(login_url = "login")
def classroom(request,class_id):
    if request.user.is_authenticated:
        us= request.user
        profile = Profile.objects.get(user=us)
        if profile.type == "Etudiant":
            classroom = Classe_etudiant.objects.get(id=class_id)
        elif profile.type == "Enseignant":
            classroom = Classroom.objects.get(id=class_id)
            
        if request.method == "POST":
            post_media = request.FILES.get("post_media")
            post_content = request.POST.get("post_content")
            if not post_media and not post_content:
                return redirect('classroom', class_id=class_id)
            if "post_media" in request.FILES and "post_content" in request.POST:
                classroom = Classroom.objects.get(id=class_id)
                Class_publication.objects.create(attachement=request.FILES["post_media"],content=request.POST["post_content"],type='annonce',classroom=classroom)
            elif"post_media" in request.FILES :
                classroom = Classroom.objects.get(id=class_id)
                Class_publication.objects.create(attachement=request.FILES["post_media"],type='annonce',classroom=classroom)
            elif "post_content" in request.POST:
                classroom = Classroom.objects.get(id=class_id)
                Class_publication.objects.create(content=request.POST["post_content"],type='annonce',classroom=classroom)
        classroompubs = reversed(Class_publication.objects.filter(classroom=class_id))    
                
    return render(request,"etudiant/classroom.html",{"classroom":classroom,"classroompubs":classroompubs})

@login_required(login_url = "login")
def classroompub(request, pub_id):
    if request.user.is_authenticated:
        pub = Class_publication.objects.get(id=pub_id)
        
        if request.method == "POST":
            if "comment" in request.POST:
                if "comment" in request.POST:
                    Class_comments.objects.create(user=request.user,content=request.POST["comment"],publication=pub)
            else:
                return redirect('classroompub', pub_id=pub_id)
        classcom=reversed(Class_comments.objects.filter(publication=pub))
        return render(request, "etudiant/classroompub.html", {"pub": pub,"classcom":classcom})

    else:
        return redirect('login')
    
@login_required(login_url = "login")
def delete_classroom(request, classroom_id):
    if request.method == 'POST':
        classroom = Classroom.objects.get(id=classroom_id)
        if request.user == classroom.enseignant.user:
            classroom.delete()
    return redirect('classrooms')

@login_required(login_url = "login")
def create_classroom(request):
    if request.user.is_authenticated:
        us= request.user
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            enseignant=Enseignant.objects.get(user=us)
            classroom = Classroom.objects.create(title=title, description=description, enseignant=enseignant)
            return redirect('classrooms')
    return render(request, 'layout/createclassroom.html')

@login_required(login_url = "login")
def delete_class_publication(request, pub_id):
    if request.method == 'POST':
        class_publication = Class_publication.objects.get(id=pub_id)
        class_publication.delete()
    return redirect('classroom', class_id=class_publication.classroom.id)
                    
@login_required(login_url = "login")
def ajouter_etudiant(request, classroom_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cne = request.POST.get('cne')
            
            classroom = Classroom.objects.get(id=classroom_id)
            
            student, created = Etudiant.objects.get_or_create(CNE=cne)
            
            if created:
                student.save()
                Classe_etudiant.objects.create(etudiant=student, classroom=classroom)
            else:
                if not Classe_etudiant.objects.filter(etudiant=student, classroom=classroom).exists():
                    Classe_etudiant.objects.create(etudiant=student, classroom=classroom)
            return redirect('ajouter_etudiant', classroom_id=classroom_id)
        else:
            all_students = Etudiant.objects.all()
            classroom_students = Classe_etudiant.objects.filter(classroom=classroom_id)
            return render(request, 'layout/ajouteretudiant.html', { "classroomstd": all_students, "classroom_id": classroom_id , "thisclassstd": classroom_students})
    return redirect('ajouter_etudiant', classroom_id=classroom_id)