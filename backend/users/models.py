from django.db import models
from django.contrib.auth.hashers import make_password
import random
import string

class Role(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.role


class Passphrase(models.Model):
    passphrase = models.CharField(max_length=4)
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='passphrase')

    def __str__(self):
        return self.passphrase


class User(models.Model):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone = models.CharField(max_length=15)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')  # Assign 'user' role by default

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Hash the password before saving the user
        if not self.password.startswith("pbkdf2_"):  # Check if password is already hashed
            self.password = make_password(self.password)

        # Assign default 'user' role if not set
        if self.role is None:
            self.role, created = Role.objects.get_or_create(role='user')

        super().save(*args, **kwargs)

        # Generate and link a random 4-letter passphrase if not present
        if not hasattr(self, 'passphrase'):
            random_passphrase = ''.join(random.choices(string.ascii_uppercase, k=4))
            Passphrase.objects.create(passphrase=random_passphrase, user=self)
