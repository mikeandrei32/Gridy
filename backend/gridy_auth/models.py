from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        RESIDENT = 'RESIDENT', 'Resident'

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.RESIDENT,
    )
        
class Resident(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    voter_status = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    

    def __str__(self):
        return f'{self.full_name}'