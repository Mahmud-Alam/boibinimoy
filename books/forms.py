from django import forms
from .models import *


class BookForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['creator','review','slug']


class CategoryForm(forms.ModelForm):    
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['slug']


class BookCommentForm(forms.ModelForm):
    class Meta:
        model = BookComment
        fields = '__all__'
        exclude = ['creator']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':100}),
        }


class ProfileBookCommentForm(forms.ModelForm):
    class Meta:
        model = BookComment
        fields = '__all__'
        exclude = ['creator']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':90}),
        }


class BookDetailsCommentForm(forms.ModelForm):
    class Meta:
        model = BookComment
        fields = '__all__'
        exclude = ['creator']
        widgets = {
          'comment': forms.Textarea(attrs={'rows':3, 'cols':70}),
        }
