

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='users')
    telephone = models.CharField(max_length=15, blank=True)
    location = models.CharField(default='Bishkek/Kyrgyzstan', max_length=100)
    points = models.IntegerField(default=0)
    donation_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True, default=0)
    sign_total = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.get_full_name()

class Signer(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=250)
    location = models.CharField(default='Bishkek/Kyrgyzstan', max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

