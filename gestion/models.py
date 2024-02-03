from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Constantes pour les rôles
STUDENT = 'STUDENT'
TEACHER = 'TEACHER'
ROLE_CHOICES = (
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email_address = models.EmailField(max_length=255, unique=True, null=True)

    def __str__(self):
        return self.user.username
# Modèle de projet
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    students = models.ManyToManyField(User, related_name='projects_as_student', blank=True)
    teachers = models.ManyToManyField(User, related_name='projects_as_teacher', blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects')

    def __str__(self):
        return self.title

# Modèle de document lié au projet
class ProjectDocument(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    document = models.FileField(upload_to='project_documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document} for {self.project}'

# Modèle de progression du projet
class ProjectProgress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone = models.CharField(max_length=100)
    description = models.TextField()
    completion_date = models.DateField()

    def __str__(self):
        return f'Milestone: {self.milestone} for {self.project}'

# Modèle d'évaluation du projet par les enseignants
class ProjectEvaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    evaluated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation_date = models.DateField(auto_now=True)
    rating = models.PositiveIntegerField()
    comments = models.TextField()

    def __str__(self):
        return f'Evaluation for {self.project} by {self.evaluated_by}'

# Modèle pour suivre la participation des étudiants à un projet
class StudentParticipation(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_participations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_participating = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.student} participation in {self.project}'

# Modèle pour suivre les enseignants associés à un projet
class TeacherAssociation(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_associations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher} associated with {self.project}'
