from rest_framework import generics
from .models import User, Role
from .serializers import UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        # Fetch the 'user' role or create it if it doesn't exist
        role, created = Role.objects.get_or_create(role='user')
        user = serializer.save(role=role)
        # The passphrase is automatically created through the User model's save method
