from django.contrib import admin
from .models import UserProfile, Project, ProjectDocument, ProjectProgress, ProjectEvaluation, StudentParticipation, TeacherAssociation

# Enregistrer le modèle UserProfile pour l'administration
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']

# Assurez-vous que les autres modèles sont également enregistrés si ce n'est pas déjà le cas
admin.site.register(Project)
admin.site.register(ProjectDocument)
admin.site.register(ProjectProgress)
admin.site.register(ProjectEvaluation)
admin.site.register(StudentParticipation)
admin.site.register(TeacherAssociation)
