from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    blog = models.TextField(null = True, blank=True)
    image = models.ImageField(null=True, blank=True)
    review = models.CharField(max_length=50, default="True", null = True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

