from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Task



class TaskForm(forms.ModelForm):
        class Meta:
                model = Task
                fields = ['title', 'description', 'completed']


        # Create your views here.
        #Registration view
        def register(request):
                if request.method == 'POST':
                        form = UserCreationForm(request.POST)
                        if form.is_valid():
                                form.save()
                                return redirect('login')
                else:
                        form = UserCreationForm()
                return render(request, "tasks/register.html",{"form": form})

        #Login view
        def user_login(request):
                if request.method == 'POST':
                        form = AuthenticationForm(data=request.POST)
                        if form.is_valid():
                                user = form.get_user()
                                login(request, user)
                                return redirect('task_list')
                else:
                        form = AuthenticationForm()
                return render(request, "tasks/login.html",{"form": form})

        #Logout view
        def user_logout(request):
                logout(request)
                return redirect('login')


        #task list view
        @login_required
        def task_list(request):
                tasks = Task.objects.all()
                return render(request, "tasks/task_list.html", {"tasks": tasks})

        def task_create(request):
                if request.method == 'POST':
                        form = TaskForm(request.POST)
                        if form.is_valid():
                                form.save()
                                return redirect('task_list')
                else:
                        form = TaskForm()
                return render(request, "tasks/task_form.html", {"form": form})
                
        def task_update(request, id):
                task = Task.objects_or_404(Task, id=id)
                if request.method == 'POST':
                        form = TaskForm(request.POST, instance=task)
                        if form.is_valid():
                                form.save()
                                return redirect('task_list')
                else:
                        form = TaskForm(instance=task)
                return render(request, "tasks/task_form.html", {"form": form})

        def task_delete(request, id):
                task = get_object_or_404(Task, id=id)
                task.delete()
                return redirect('task_list')