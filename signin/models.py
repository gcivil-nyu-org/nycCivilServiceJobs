from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# class User(AbstractUser):
#     username = models.CharField(max_length=30, primary_key=True)
#     email_address = models.EmailField(blank=True, null=True, unique=True)
#     first_name = models.CharField(max_length=30, blank=True, null=True)
#     last_name = models.CharField(max_length=30, blank=True, null=True)
#     staff_status = models.BooleanField(default=False)
#     dob = models.DateTimeField('date of birth')
#
#     def __str__(self):
#         return '{} {} {} {} {} {} {}'.format(self.username, self.email_address,
#                                              self.first_name, self.last_name, self.staff_status,
#                                              self.account_type, self.dob)


# class User(AbstractUser):
#     # is_hiringmanager = models.BooleanField(default=False)
#     user = models.OneToOneField(AbstractUser, null=True, blank=True, on_delete=models.CASCADE),
#     email_address = models.EmailField(unique=True)
#
#
#     def __str__(self):
#         return self.email
#
#
# class User_Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='user_profile')
#     security_question = models.CharField(max_length=20)
