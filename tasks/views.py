from django.http import HttpResponse,HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.forms import LoginUserForm
from django.urls import reverse_lazy, reverse

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponseRedirect(reverse('login_user'))
    else:
        form = LoginUserForm()
        return render(request, 'registration/login.html', {'form': form})


def home(request):
    return render(request, 'home.html')  #


@login_required
def tasks_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
