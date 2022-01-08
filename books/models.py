from django.db import models
from users.models import Customer
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    # CATEGORY = (
    #     ('Action and Adventure','Action and Adventure'),
    #     ('Biographies and Autobiographies','Biographies and Autobiographies'),
    #     ('Classics','Classics'),
    #     ('Comic','Comic'),
    #     ('Cookbooks','Cookbooks'),
    #     ('Detective and Mystery','Detective and Mystery'),
    #     ('Essays','Essays'),
    #     ('Fantasy','Fantasy'),
    #     ('History','History'),
    #     ('Historical Fiction','Historical Fiction'),
    #     ('Horror','Horror'),
    #     ('Literary Fiction','Literary Fiction'),
    #     ('Poetry','Poetry'),
    #     ('Romance','Romance'),
    #     ('Self-Help','Self-Help'),
    #     ('Science Fiction','Science Fiction'),
    #     ('Short Stories','Short Stories'),
    #     ('Suspense and Thrillers','Suspense and Thrillers'),
    #     ('True Crime','True Crime'),
    # )

    EXCHANGE = (
        ('Yes','Yes'),
        ('No','No'),
    )

    creator = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    edition = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(default='default.jpg', null=True, blank=True)
    review = models.CharField(max_length=50, default="False", null = True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    description = models.TextField(null = True, blank=True)
    exchange = models.CharField(max_length=200,choices=EXCHANGE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def bookImageURL(self):
        try:
            img = self.image.url
        except:
            img = ''
        return img


class BookComment(models.Model):
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

