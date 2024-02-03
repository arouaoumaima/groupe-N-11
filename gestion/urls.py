
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'gestion'
urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/new/', views.create_project, name='create_project'),
    path('project/<int:project_id>/add_document/', views.add_document, name='add_document'),
    path('project/<int:project_id>/add_progress/', views.add_progress, name='add_progress'),
    path('project/<int:project_id>/evaluate/', views.evaluate_project, name='evaluate_project'),
    path('project/<int:project_id>/follow_student/', views.follow_student, name='follow_student'),
    path('project/<int:project_id>/unfollow_student/', views.unfollow_student, name='unfollow_student'),
    path('project/<int:project_id>/follow_teacher/', views.follow_teacher, name='follow_teacher'),
    path('project/<int:project_id>/unfollow_teacher/', views.unfollow_teacher, name='unfollow_teacher'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('project/<int:project_id>/modify/', views.modify_project, name='modify_project'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    # autres chemins d'URL selon vos besoins...
    path('project/<int:project_id>/modify_document/<int:document_id>/', views.modify_document, name='modify_document'),
    path('project/<int:project_id>/delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('project/<int:project_id>/download_document/<int:document_id>/', views.download_document, name='download_document'),
    path('profile', views.profile, name='profile'),




]
