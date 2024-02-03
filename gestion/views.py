from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import UserProfile, Project, ProjectDocument, ProjectProgress, ProjectEvaluation, StudentParticipation, TeacherAssociation
from .forms import ProjectForm, DocumentForm, ProgressForm, EvaluationForm, CustomUserCreationForm
from .decorators import student_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
import os
import logging
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied

# Constants for roles
STUDENT = 'STUDENT'
TEACHER = 'TEACHER'

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    documents = ProjectDocument.objects.filter(project=project)
    progress = ProjectProgress.objects.filter(project=project)
    evaluations = ProjectEvaluation.objects.filter(project=project)
    student_participations = StudentParticipation.objects.filter(project=project, is_participating=True)

    return render(request, 'project_detail.html', {
        'project': project,
        'documents': documents,
        'progress': progress,
        'evaluations': evaluations,
        'student_participations': student_participations
    })

@login_required
def create_project(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role != 'STUDENT':  # Assuming 'STUDENT' is the role value for students
        messages.error(request, "Seuls les étudiants peuvent créer des projets.")
        return redirect('gestion:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user  # Set the creator to the current user
            project.save()
            messages.success(request, "Projet créé avec succès.")
            return redirect('gestion:project_list')
    else:
        form = ProjectForm()

    return render(request, 'create_project.html', {'form': form})

@student_required
@login_required
def modify_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('gestion:project_detail', project_id=project_id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'modify_project.html', {'form': form ,'project': project})
@student_required
@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('gestion:project_list')

    return render(request, 'project_confirm_delete.html', {'project': project})



@login_required
def add_document(request, project_id):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Assuming STUDENT is a constant representing the student role
    if user_profile.role != STUDENT:
        raise PermissionDenied("Seuls les étudiants peuvent ajouter des documents.")
    
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.project = project
            document.uploaded_by = request.user
            document.save()
            messages.success(request, "Document ajouté avec succès.")
            return redirect('gestion:project_detail', project_id=project_id)
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = DocumentForm()
    
    return render(request, 'add_document.html', {'form': form, 'project': project})
    
@login_required
@student_required
def modify_document(request, project_id, document_id):
    project = get_object_or_404(Project, id=project_id)
    document = get_object_or_404(ProjectDocument, id=document_id, project_id=project_id)

    if request.user != document.uploaded_by:
        messages.error(request, "You do not have permission to modify this document.")
        return redirect('gestion:project_detail', project_id=project.id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Document modified successfully!")
            return redirect('gestion:project_detail', project_id=project.id)
    else:
        form = DocumentForm(instance=document)

    return render(request, 'modify_document.html', {'form': form, 'document': document, 'project': project})

@student_required
@login_required
def delete_document(request, project_id, document_id):
    document = get_object_or_404(ProjectDocument, id=document_id, project_id=project_id)

    if request.user != document.uploaded_by:
        messages.error(request, "You do not have permission to delete this document.")
        return redirect('gestion:project_detail', project_id=project_id)

    if request.method == 'POST':
        document.delete()
        messages.success(request, "Document deleted successfully!")
        return redirect('gestion:project_detail', project_id=project_id)

    return render(request, 'delete_document_confirm.html', {'document': document})



@login_required
def add_progress(request, project_id):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role != STUDENT:
        messages.error(request, "Seuls les étudiants peuvent ajouter des informations de progression.")
        return redirect('gestion:project_detail', project_id=project_id)

    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.project = project
            progress.save()
            messages.success(request, "Progression ajoutée avec succès.")
            return redirect('gestion:project_detail', project_id=project_id)
    else:
        form = ProgressForm()
    return render(request, 'add_progress.html', {'form': form, 'project': project})

@login_required
def evaluate_project(request, project_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.role != 'TEACHER':  # Replace 'TEACHER' with your actual role value
        messages.error(request, "Seuls les enseignants peuvent évaluer des projets.")
        return redirect('gestion:project_list')

    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.project = project
            evaluation.evaluated_by = request.user
            evaluation.save()
            messages.success(request, "Évaluation ajoutée avec succès.")
            return redirect('gestion:project_detail', project_id=project_id)
    else:
        form = EvaluationForm()

    return render(request, 'evaluate_project.html', {'form': form, 'project': project})

@login_required
def follow_student(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    StudentParticipation.objects.create(student=request.user, project=project, is_participating=True)
    messages.success(request, "Participation enregistrée.")
    return redirect('gestion:project_detail', project_id=project.pk)

@login_required
def unfollow_student(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    participation = get_object_or_404(StudentParticipation, student=request.user, project=project)
    participation.is_participating = False
    participation.save()
    messages.success(request, "Participation retirée.")
    return redirect('gestion:project_detail', project_id=project.pk)

@login_required
def follow_teacher(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    TeacherAssociation.objects.create(teacher=request.user, project=project)
    messages.success(request, "Suivi enregistré.")
    return redirect('gestion:project_detail', project_id=project.pk)

@login_required
def unfollow_teacher(request, project_id):
    # First, retrieve the Project object associated with project_id
    project = get_object_or_404(Project, id=project_id)

    # Then, attempt to retrieve the TeacherAssociation object
    try:
        teacher_association = TeacherAssociation.objects.get(project=project, teacher=request.user)
    except TeacherAssociation.DoesNotExist:
        # Handle the case where the TeacherAssociation doesn't exist
        messages.error(request, "You are not following this teacher.")
        return redirect('gestion:project_detail', project_id=project_id)

    # Perform the unfollow operation
    teacher_association.delete()

    messages.success(request, "You have successfully unfollowed this teacher.")
    return redirect('gestion:project_detail', project_id=project_id)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role, email_address=user.email)
            messages.success(request, "Inscription réussie. Veuillez vous connecter.")
            return redirect('gestion:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie.")
                return redirect('gestion:project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
# Set up logging
logger = logging.getLogger(__name__)

@login_required
def download_document(request, project_id, document_id):
    # Ensure the document is associated with the given project
    project = get_object_or_404(Project, id=project_id)
    document = get_object_or_404(ProjectDocument, id=document_id, project=project)

    # Logging the download action
    logger.info(f"User {request.user.username} is downloading the document: {document.document.name} from project: {project.title}")

    # Get the file path from the document
    file_path = document.document.path  # Using 'document' field from your model

    # Check if file exists in the path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            # Read the file and create an HTTP response with it
            response = HttpResponse(fh.read(), content_type="application/force-download")
            # Set the content disposition to attachment with the file name
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    
    # If the file does not exist, raise a 404 error
    raise Http404
@login_required
def profile(request):
    # The context dictionary can pass additional information to the template
    context = {
        'user': request.user,
        # Add any additional context you might need
    }
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('gestion:login')  # Replace 'login' with the name of your login URL pattern