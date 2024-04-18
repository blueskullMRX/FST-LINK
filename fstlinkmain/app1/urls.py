from django.urls import path
from django.contrib import admin
from . import views

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),

    path('chat/<int:chatroom_id>', views.chat, name='chat'),
    path('chat/', views.chat),

    path('profile/<username>',views.profile,name="profile_username"),
    path('profile_search',views.search),
    path('profile/',views.profile,name='profile'),
    path('profilesettings/',views.profilesettings,name='profilesettings'),

    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path("logout/",views.logout,name="logout"),


    path('dashboard/', views.dashboardetd, name='dashboardetd'),
    path('dashboard/home', views.dashboardhome, name='dashboardhome'),
    path('classrooms/',views.classrooms,name='classrooms'),
    path('classroompub/<int:pub_id>/', views.classroompub, name='classroompub'),
    path('classroom/<class_id>/',views.classroom,name='classroom'),
    path('delete-classroom/<int:classroom_id>/', views.delete_classroom, name='delete_classroom'),
    path('create_classroom/', views.create_classroom, name='create_classroom'),
    path('ajouter_etudiant/<int:classroom_id>', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('delete-class-publication/<int:pub_id>/', views.delete_class_publication, name='delete_class_publication'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)