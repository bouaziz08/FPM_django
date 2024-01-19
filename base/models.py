from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    priority = models.TextField( blank=True, default="0", max_length=1, choices=[('0', 'default'), ('1', 'low'), ('2', 'medium'), ('3', 'high')])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

