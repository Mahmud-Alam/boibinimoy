# Generated by Django 3.2.6 on 2021-11-22 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211123_0239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='Occupation',
            new_name='occupation',
        ),
    ]
