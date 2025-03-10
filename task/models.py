from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("P", "Pending"),
        ("IP", "In Progress"),
        ("C", "Completed"),
        ("A", "Archived"),
    ]

    PRIORITY_CHOICES = [
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
    ]

    CATEGORY_CHOICES = [
        ("W", "Work"),
        ("P", "Personal"),
        ("H", "Home"),
        ("O", "Other"),
    ]

    title = models.CharField(max_length=200)
    # description = models.TextField(blank=True, null=True)
    description = SummernoteTextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="P")
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default="O")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.status == "C" and self.completed_date is None:
            self.completed_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]
