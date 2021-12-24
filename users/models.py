from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

class Customer(models.Model):

    GENDER_TYPE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )

    OCCUPATION_TYPE = (
        ('Student','Student'),
        ('Job-Holder','Job-Holder'),
    )

    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='profile-white.png', null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    occupation = models.CharField(max_length=50,choices=OCCUPATION_TYPE, null=True,blank=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE, null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username.username

    @property
    def customerImageURL(self):
        try:
            img = self.profile_pic.url
        except:
            img = ''
        return img


class Manager(models.Model):

    GENDER_TYPE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )

    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='profile-white.png', null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE, null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username.username

    @property
    def managerImageURL(self):
        try:
            img = self.profile_pic.url
        except:
            img = ''
        return img


class Admin(models.Model):

    GENDER_TYPE = (
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    )

    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='profile-white.png', null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=50,choices=GENDER_TYPE, null=True,blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username.username

    @property
    def adminImageURL(self):
        try:
            img = self.profile_pic.url
        except:
            img = ''
        return img

