from rest_framework import serializers
from .models import User, Role, Passphrase

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
