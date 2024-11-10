from rest_framework import serializers
from .models import User, Role, Passphrase

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

class PassphraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passphrase
        fields = ['passphrase']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)  # Nested serializer for Role, read-only
    passphrase = PassphraseSerializer(read_only=True)  # Nested serializer for Passphrase, read-only
    password = serializers.CharField(write_only=True)  # Password is write-only

    class Meta:
        model = User
        fields = ['email', 'fname', 'password', 'phone', 'role', 'passphrase']
        
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    passphrase = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        passphrase = data.get('passphrase')

        # Attempt to get the user by email
        try:
            user = User.objects.get(email=email)
            print(f"[DEBUG] User found with email: {email}")  # Debugging line
        except User.DoesNotExist:
            print(f"[DEBUG] No user found with email: {email}")  # Debugging line
            raise serializers.ValidationError("Invalid email or password.")

        # Check if password matches
        if not check_password(password, user.password):
            print(f"[DEBUG] Password check failed for user: {email}")  # Debugging line
            raise serializers.ValidationError("Invalid email or password.")
        else:
            print(f"[DEBUG] Password check passed for user: {email}")  # Debugging line

        # Check the passphrase
        if not user.passphrase or user.passphrase.passphrase != passphrase:
            print(f"[DEBUG] Passphrase check failed for user: {email}")  # Debugging line
            raise serializers.ValidationError("Invalid passphrase.")
        else:
            print(f"[DEBUG] Passphrase check passed for user: {email}")  # Debugging line

        # Generate JWT token upon successful login
        refresh = RefreshToken.for_user(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"] = user.id

        print(f"[DEBUG] Login successful for user: {email}")  # Debugging line
        return data
    