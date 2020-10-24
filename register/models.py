from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    dob = models.DateField("Date of Birth", null=True, blank=True)
    is_hiring_manager = models.BooleanField("Hiring Manager", default=False)
