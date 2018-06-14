from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from tracker.middleware import current_user


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
    title = models.CharField(max_length=200, null=False)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE,  editable=False, default=current_user.get_current_user)
    assigned_to = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    created = models.DateTimeField('date created', default=datetime.now)
    closed = models.DateTimeField('date closed', null=True, blank=True)

    class Meta:
        permissions = (
            ("is_superuser", "Can add, remove and edit Issues"),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '%d' % self.id

