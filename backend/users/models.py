from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.email
