from django.db import models

from django.contrib.auth.models import User

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(default=1, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    updation_date = models.DateTimeField(auto_now=True)


class TaskEmail(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    mail_time = models.IntegerField(default=0)
