from django.db import models
from django.conf import settings


# Create your models here.


class ProjectStatusModel(models.TextChoices):
    PLANNING = 'PLANNING', 'planning'
    IN_PROGRESS = 'IN_PROGRESS', 'in progress'
    COMPLETED = 'COMPLETED', 'completed'


class ProjectModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ProjectStatusModel.choices,
        default=ProjectStatusModel.PLANNING
    )

    def __str__(self):
        return self.title


