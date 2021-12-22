# from django.db.models.signals import post_save
# from django.contrib.auth.models import User, Group
# from .models import *

# def customer_profile(sender, instance, created, **kwargs):
#     if created:
#         group = Group.objects.get(name='customer')
#         instance.groups.add(group)

#         Customer.objects.create(username=instance, first_name=instance.first_name, last_name=instance.last_name,email=instance.email)
#         print(instance,"'s Profile has been created successfully!")
    
# post_save.connect(customer_profile, sender=User)

