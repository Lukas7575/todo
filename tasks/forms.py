from django import forms
from django.contrib.auth.models import User

from .models import Task


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status']
