from django.db import models
from django.conf import settings
from Projects.models import ProjectModel
# Create your models here.

class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        'Projects.ProjectModel',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('DONE', 'Done'),
        ],
        default='TODO',
    )
    priority = models.CharField(
        max_length=10,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),

    ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

