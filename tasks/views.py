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


# #task list view
# @login_required
# def task_list(request):
#         tasks = Task.objects.filter(user=request.user) #Only get tasks belonging to the logged in user
#         return render(request, "tasks/task_list.html", {"tasks": tasks})



# @login_required       
# def task_update(request, id):
#         task = get_object_or_404(Task, id=id, user=request.user) #Ensure the task belongs to the logged in user
#         if request.method == 'POST':
#                 form = TaskForm(request.POST, instance=task)
#                 if form.is_valid():
#                         form.save()
#                         return redirect('task_list')
#         else:
#                 form = TaskForm(instance=task)
#         return render(request, "tasks/task_form.html", {"form": form})
# @login_required
# def task_delete(request, id):
#         task = get_object_or_404(Task, id=id, user=request.user) #Ensure the user can only delete their own tasks
#         task.delete()
#         return redirect('task_list')

def is_admin(user):
        return user.is_superuser or user.is_staff

@login_required
def task_list(request):
        #if admin show all tasks
        if is_admin(request.user):
                tasks = Task.objects.all()
                is_admin_view = True
        else:
                #Regular users only see their own tasks
                tasks = Task.objects.filter(user=request.user)
                is_admin_view = False

        return render(request, "tasks/task_list.html", {"tasks": tasks, "is_admin_view": is_admin_view})

@login_required
def task_create(request):
        if request.method == 'POST':
                form = TaskForm(request.POST)
                if form.is_valid():
                        task = form.save(commit=False) #Don't save to database yet
                        task.user = request.user #Assign the logged in user to the task
                        task.save() #Now save to database
                        return redirect('task_list')
        else:
                form = TaskForm()
        return render(request, "tasks/task_form.html", {"form": form})

@login_required
def task_update(request, id):
        #if user is admin they can update any task
        if is_admin(request.user):
                task = get_object_or_404(Task, id=id)
        else:
                #Regular users can only update their own tasks
                task = get_object_or_404(Task, id=id, user=request.user)
        if request.method == 'POST':
                form = TaskForm(request.POST, instance=task)
                if form.is_valid():
                        form.save()
                        return redirect('task_list')
        else:
                form = TaskForm(instance=task)  
        return render(request, "tasks/task_form.html", {"form": form})

@login_required
def task_delete(request, id):
        #if user is admin they can delete any task
        if is_admin(request.user):
                task = get_object_or_404(Task, id=id)
        else:
                #Regular users can only delete their own tasks
                task = get_object_or_404(Task, id=id, user=request.user)
        task.delete()
        return redirect('task_list')
        
