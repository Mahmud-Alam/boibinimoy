from django.db.models import fields
import django_filters
from django_filters import CharFilter
from .models import *

class BookFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name",lookup_expr='icontains')
    author = CharFilter(field_name="author",lookup_expr='icontains')
    edition = CharFilter(field_name="edition",lookup_expr='icontains')
    class Meta:
        model = Book
        fields = ['name','author','edition','category','exchange']
        # exclude = ['creator', 'slug','image','description','price','created']