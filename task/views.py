from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm, LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from .forms import RegistrationForm

# from .forms import LoginForm


def home(request):
    return render(request, "task/home.html")


def about(request):
    return render(request, "task/about.html")


@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    context = {"tasks": tasks, "form": form}
    return render(request, "task/tasks.html", context)


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Set the user field
            task.save()
        return redirect("/tasks/")
    return redirect("/tasks/")


@login_required
def update_task(request, p_key):
    task = get_object_or_404(Task, id=p_key, user=request.user)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("/tasks/")

    context = {"form": form}
    return render(request, "task/update_task.html", context)


@login_required
def delete_task(request, p_key):
    task = get_object_or_404(Task, id=p_key, user=request.user)
    if request.method == "POST":
        task.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "task/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "task/login.html"
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = "home"
