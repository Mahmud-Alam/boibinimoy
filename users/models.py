from django.db import models
from django.db.models.base import Model
# from django.contrib.auth.models import User

class Customer(models.Model):
    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='profile.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    CATEGORY = (
        ('Action and Adventure','Action and Adventure'),
        ('Biographies and Autobiographies','Biographies and Autobiographies'),
        ('Classics','Classics'),
        ('Comic','Comic'),
        ('Cookbooks','Cookbooks'),
        ('Detective and Mystery','Detective and Mystery'),
        ('Essays','Essays'),
        ('Fantasy','Fantasy'),
        ('History','History'),
        ('Historical Fiction','Historical Fiction'),
        ('Horror','Horror'),
        ('Literary Fiction','Literary Fiction'),
        ('Poetry','Poetry'),
        ('Romance','Romance'),
        ('Self-Help','Self-Help'),
        ('Science Fiction','Science Fiction'),
        ('Short Stories','Short Stories'),
        ('Suspense and Thrillers','Suspense and Thrillers'),
        ('True Crime','True Crime'),
    )

    EXCHANGE = (
        ('Yes','Yes'),
        ('No','No'),
    )

    name = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    edition = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200,choices=CATEGORY, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    exchange = models.CharField(max_length=200,choices=EXCHANGE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

