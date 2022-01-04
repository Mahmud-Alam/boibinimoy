from django.db import models
from django.contrib.auth.models import User
from users.models import *

class CustomerBlog(models.Model):
    creator = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    blog = models.TextField(null = True, blank=True)
    image = models.ImageField(null=True, blank=True)
    review = models.CharField(max_length=50, default="False", null = True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ManagerBlog(models.Model):
    creator = models.ForeignKey(Manager, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    blog = models.TextField(null = True, blank=True)
    image = models.ImageField(null=True, blank=True)
    review = models.CharField(max_length=50, default="True", null = True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
