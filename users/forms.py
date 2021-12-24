from django.db import models
from django.forms import ModelForm, fields
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['username','email']

class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
        exclude = ['username','email']

class AdminForm(ModelForm):
    class Meta:
        model = Manager
        fields = '__all__'
        exclude = ['username','email']
