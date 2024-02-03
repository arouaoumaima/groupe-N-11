from django import forms
from .models import Project, ProjectDocument, ProjectProgress, ProjectEvaluation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, ROLE_CHOICES
from django.core.exceptions import ValidationError

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'students', 'teachers']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # Filter the student field to only show users with the student role
        self.fields['students'].queryset = User.objects.filter(userprofile__role='STUDENT')

        # Filter the teacher field to only show users with the teacher role
        self.fields['teachers'].queryset = User.objects.filter(userprofile__role='TEACHER')
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = ProjectDocument
        fields = ['document']

class ProgressForm(forms.ModelForm):
    class Meta:
        model = ProjectProgress
        fields = ['milestone', 'description', 'completion_date']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = ProjectEvaluation
        fields = ['rating', 'comments']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    