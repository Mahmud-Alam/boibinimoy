# Generated by Django 3.2.6 on 2021-11-22 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_occupation_customer_occupation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='fName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='lName',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='username',
        ),
    ]
