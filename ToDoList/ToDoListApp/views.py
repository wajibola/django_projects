from django.http import HttpResponseRedirect

from ToDoListApp.forms.forms import TaskForm
from .models import Task, Category
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.timezone import now

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Registration view
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'todolist/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("todolist:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'todolist/user_registration_bootstrap.html', context)


# Login view
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('todolist:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'todolist/user_login_bootstrap.html', context)
    else:
        return render(request, 'todolist/user_login_bootstrap.html', context)


# Logout view
def logout_request(request):
    logout(request)
    return redirect('todolist:index')


# Create task view
def create_task(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'todolist/create_task_bootstrap.html', context)
    
    elif request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category_name = request.POST['category']
        duedate = request.POST['duedate']

        # if not (name and description and category_name and duedate):
        #     messages.error(request, "All fields are required.")
        #     return render(request, 'todolist/create_task_bootstrap.html')
        
        # Check if a task with the same name already exists
        if Task.objects.filter(name=name, category__name=category_name).exists():
            messages.error(request, f"A task with name '{name}' and category '{category_name}' already exists.")
            return render(request, 'todolist/create_task_bootstrap.html')

        category, _ = Category.objects.get_or_create(name=category_name, user=request.user)
        
        task = Task.objects.create(
            name=name,
            description=description,
            due_date=duedate,
            category=category,
            user=request.user
        )

        # messages.success(request, "Task created successfully.")
        return redirect('todolist:index')


# Task List view
class TaskListView(generic.ListView):
    template_name = 'todolist/task_list_bootstrap.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(user=user).order_by('-created_at')[:10]


# Task detail view
class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'todolist/tast_detail_bootstrap.html'


# Task list  by category view
class TaskListByCategoryView(generic.ListView):
    template_name = 'todolist/task_list_bootstrap.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()
        
        category_name = self.kwargs.get('category_name', None)
        category = Category.objects.filter(name=category_name).first()
        
        if not category:
            return Task.objects.none()
        
        return Task.objects.filter(user=user, category=category).order_by('-created_at')[:10]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs.get('category_name')
        return context


# Update task view
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            category_name = cleaned_data['category_name']
            
            # Ensure the category exists or create a new one
            category, _ = Category.objects.get_or_create(name=category_name, user=request.user)
            
            # Check if a task with the same name and category already exists
            if Task.objects.filter(category=category, name=cleaned_data['name']).exclude(id=task.id).exists():
                messages.error(request, f"A task with name '{cleaned_data['name']}' and category '{category_name}' already exists.")
            else:
                task.name = cleaned_data['name']
                task.description = cleaned_data['description']
                task.status = cleaned_data['status']
                task.due_date = cleaned_data['due_date']
                task.category = category
                task.updated_at = now()
                task.save()

                messages.success(request, "Task updated successfully.")
                return redirect('todolist:task_details', pk=task.id)
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = TaskForm(instance=task)

    categories = Category.objects.all()
    context = {
        'task': task,
        'form': form,
        'categories': categories,
    }

    return render(request, 'todolist/tast_detail_bootstrap.html', context)


# Delete task view
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

