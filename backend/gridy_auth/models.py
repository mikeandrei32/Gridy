from django.utils import choices
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin',
        RESIDENT = 'RESIDENT', 'Resident',

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.RESIDENT,
    )
        
