# ritualUS/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    dni = models.CharField(max_length=9, unique=True, null=False)

    def __str__(self):
        return self.username
    
    

