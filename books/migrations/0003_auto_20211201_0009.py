# Generated by Django 3.2.6 on 2021-11-30 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_delete_book'),
        ('books', '0002_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer'),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
