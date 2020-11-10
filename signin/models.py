from django.db import models
from register.models import User
from examresults.models import CivilServicesTitle

# Create your models here.


class UsersCurrentCivilServiceTitle(models.Model):
    civil_service_title = models.ForeignKey(
        CivilServicesTitle, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("civil_service_title", "user")


class UsersInterestedCivilServiceTitle(models.Model):
    civil_service_title = models.ForeignKey(
        CivilServicesTitle, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_number = models.CharField(max_length=200)

    class Meta:
        unique_together = ("exam_number", "user")
