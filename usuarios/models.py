from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        ('GESTOR', 'Gestor'),
        ('MOTORISTA', 'Motorista'),
        ('CLIENTE', 'Cliente'),
    )
    user_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='CLIENTE')
