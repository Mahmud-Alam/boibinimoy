# Generated by Django 3.2.6 on 2021-11-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('edition', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, choices=[('Action and Adventure', 'Action and Adventure'), ('Biographies and Autobiographies', 'Biographies and Autobiographies'), ('Classics', 'Classics'), ('Comic', 'Comic'), ('Cookbooks', 'Cookbooks'), ('Detective and Mystery', 'Detective and Mystery'), ('Essays', 'Essays'), ('Fantasy', 'Fantasy'), ('History', 'History'), ('Historical Fiction', 'Historical Fiction'), ('Horror', 'Horror'), ('Literary Fiction', 'Literary Fiction'), ('Poetry', 'Poetry'), ('Romance', 'Romance'), ('Self-Help', 'Self-Help'), ('Science Fiction', 'Science Fiction'), ('Short Stories', 'Short Stories'), ('Suspense and Thrillers', 'Suspense and Thrillers'), ('True Crime', 'True Crime')], max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('exchange', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=200, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='profile.png', null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
