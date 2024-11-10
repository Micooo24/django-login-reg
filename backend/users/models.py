from django.db import models
from django.contrib.auth.hashers import make_password
import random
import string
from django.core.exceptions import ValidationError
import hashlib

class Role(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.role


class Passphrase(models.Model):
    passphrase = models.CharField(max_length=100)  
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='passphrase')

    #para linisin yung input and i check kung 4 ba talaga yung words
    def clean(self):
        
        word_count = len(self.passphrase.split())
        if word_count > 4:
            raise ValidationError("Passphrase must not exceed 4 words.")
    
    def save(self, *args, **kwargs):
        #pang hash ng passphrase
        if not self.passphrase.isalnum() or len(self.passphrase) != 64:  
            hashed_passphrase = hashlib.sha256(self.passphrase.encode()).hexdigest()
            self.passphrase = hashed_passphrase
        super().save(*args, **kwargs)

    def __str__(self):
        return self.passphrase


class User(models.Model):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed passwords
    phone = models.CharField(max_length=15)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')  # Assign 'user' role by default

    def __str__(self):
        return self

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

class Password(models.Model):
    password = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
       
        if not self.password.startswith('pbkdf2_'):  
            self.password = make_password(self.password)
        super(Account, self).save(*args, **kwargs)
    
    def __str__(self):
        return self
            
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.OneToOneField(Password, on_delete=models.CASCADE, related_name='accounts')
    
    def __str__(self):
        return self
    
    
    
class Analysis(models.Model):
    password = models.OneToOneField(Password, on_delete=models.CASCADE, related_name='analysis')
    entropy = models.FloatField(null=True, blank=True)
    estimated_cracking_time = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=100)
    
    def __str__(self):
        return self
    

# NOt MODEL RELATED, I GUESS SA CONTROLLER TONG FUNCTION ILALAGAY
            # def calculate_entropy(password):
            #     """Calculate password entropy in bits."""
            #     length = len(password)
            #     pool_size = 0
                
            #     # Estimate pool size based on character types
            #     if any(c.islower() for c in password): pool_size += 26
            #     if any(c.isupper() for c in password): pool_size += 26
            #     if any(c.isdigit() for c in password): pool_size += 10
            #     if any(c in '!@#$%^&*()-_=+[]{};:,.<>/?' for c in password): pool_size += 32  # Special chars
                
            #     # Entropy formula: length * log2(pool_size)
            #     entropy = length * math.log2(pool_size) if pool_size > 0 else 0
            #     return entropy
# ====================================================================
    
    
