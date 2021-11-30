from django import forms

from .models import *


class BookForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['creator', 'slug']
