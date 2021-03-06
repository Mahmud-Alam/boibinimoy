# Generated by Django 3.2.6 on 2022-01-04 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_admin'),
        ('blogs', '0003_alter_blog_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('blog', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('review', models.CharField(blank=True, default='False', max_length=50, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('blog', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('review', models.CharField(blank=True, default='True', max_length=50, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.manager')),
            ],
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
