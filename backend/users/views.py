# Description: Views for the users app.

from rest_framework import generics
from .models import User, Role
from .serializers import UserSerializer, LoginSerializer

# for login process
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



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

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            print(f"[DEBUG] Login data validated for email: {request.data.get('email')}")  # Debugging line
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            print(f"[DEBUG] Login validation failed for email: {request.data.get('email')}")  # Debugging line
            print(f"[DEBUG] Errors: {serializer.errors}")  # Debugging line
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        