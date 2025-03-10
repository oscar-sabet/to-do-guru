from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm, LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Count

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
    tasks = Task.objects.filter(user=request.user).order_by("-status", "-created")
    form = TaskForm()

    context = {"tasks": tasks, "form": form}
    return render(request, "task/tasks.html", context)


@login_required
def task_board(request):
    order_by = request.GET.get("order_by", "status")  # Default ordering by status
    tasks = Task.objects.filter(user=request.user).order_by(order_by)
    not_started_tasks = tasks.filter(status="P")
    in_progress_tasks = tasks.filter(status="IP")
    completed_tasks = tasks.filter(status="C")
    return render(
        request,
        "task/task_board.html",
        {
            "not_started_tasks": not_started_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "order_by": order_by,
        },
    )


@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.status = request.POST.get("status")
        task.save()
    return redirect("task_board")


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


@login_required
def task_report(request):
    tasks = Task.objects.filter(user=request.user)
    status_counts = tasks.values("status").annotate(count=Count("status"))
    priority_counts = tasks.values("priority").annotate(count=Count("priority"))
    category_counts = tasks.values("category").annotate(count=Count("category"))

    # Generate a pie chart for task status
    status_labels = [
        Task(status=status["status"]).get_status_display() for status in status_counts
    ]
    status_sizes = [status["count"] for status in status_counts]
    plt.figure(figsize=(6, 6))
    plt.pie(status_sizes, labels=status_labels, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    status_chart = io.BytesIO()
    plt.savefig(status_chart, format="png")
    status_chart.seek(0)
    status_chart_base64 = base64.b64encode(status_chart.read()).decode("utf-8")

    # Generate a bar chart for task priority
    priority_labels = [
        Task(priority=priority["priority"]).get_priority_display()
        for priority in priority_counts
    ]
    priority_sizes = [priority["count"] for priority in priority_counts]
    plt.figure(figsize=(8, 6))
    plt.bar(priority_labels, priority_sizes, color="skyblue")
    plt.xlabel("Priority")
    plt.ylabel("Count")
    plt.title("Task Priority Distribution")
    priority_chart = io.BytesIO()
    plt.savefig(priority_chart, format="png")
    priority_chart.seek(0)
    priority_chart_base64 = base64.b64encode(priority_chart.read()).decode("utf-8")

    # Generate a bar chart for task category
    category_labels = [
        Task(category=category["category"]).get_category_display()
        for category in category_counts
    ]
    category_sizes = [category["count"] for category in category_counts]
    plt.figure(figsize=(8, 6))
    plt.bar(category_labels, category_sizes, color="lightgreen")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.title("Task Category Distribution")
    category_chart = io.BytesIO()
    plt.savefig(category_chart, format="png")
    category_chart.seek(0)
    category_chart_base64 = base64.b64encode(category_chart.read()).decode("utf-8")

    context = {
        "status_chart": status_chart_base64,
        "priority_chart": priority_chart_base64,
        "category_chart": category_chart_base64,
    }
    return render(request, "task/task_report.html", context)


class CustomLoginView(LoginView):
    template_name = "task/login.html"
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    next_page = "home"
