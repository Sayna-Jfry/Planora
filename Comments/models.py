from django.db import models
from Tasks.models import TaskModel


from django.conf import settings


# Create your models here.


class CommentModel(models.Model):
    content = models.TextField()
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return  f'{self.author.username} - {self.task.title} - {self.content}'

