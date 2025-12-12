from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from .models import User
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
