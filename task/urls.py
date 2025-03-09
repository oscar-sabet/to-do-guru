from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page (index)
    path("about/", views.about, name="about"),  # About page
    path("tasks/", views.index, name="index"),  # Task list page
    path("update_task/<str:p_key>", views.update_task, name="update_task"),
    path("delete/<str:p_key>/", views.delete_task, name="delete_task"),
    path("create/", views.create_task, name="create_task"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("task_board/", views.task_board, name="task_board"),
    path(
        "update_task_status/<int:task_id>/",
        views.update_task_status,
        name="update_task_status",
    ),
    path("task_report/", views.task_report, name="task_report"),
    path("summernote/", include("django_summernote.urls")),
]
