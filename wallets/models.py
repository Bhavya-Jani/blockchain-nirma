from django.db import models
from django.contrib.auth.hashers import make_password

class Wallet(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed password
    blockchain_network = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        """ Hash password before saving """
        self.password = make_password(self.password)  # Hash the password
        super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
