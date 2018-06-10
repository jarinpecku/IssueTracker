from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "statuses"


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class Issue(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField('date created')
    closed = models.DateTimeField('date closed')

    def __str__(self):
        return self.title



