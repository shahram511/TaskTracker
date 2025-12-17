from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer
from .models import User
from .serializers import ProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser 
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'avatar': {
                    'type': 'string',
                    'format': 'binary',
                    'description': 'Upload your avatar image'
                },
                'bio': {
                    'type': 'string',
                    'description': 'Your biography'
                }
            }
        }
    }
)
class ProfileView(generics.RetrieveUpdateAPIView):    
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user.profile
    

def login_page_view(request):
    return render(request, 'login.html')
    
def tasks_page_view(request):
    return render (request, 'tasks.html')
    
