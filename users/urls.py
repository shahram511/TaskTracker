from django.urls import path
from .views import RegisterView, ProfileView, login_page_view, tasks_page_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('login-panel/', login_page_view, name='login-page'),   
    path('tasks-panel/', tasks_page_view, name='tasks-page') 
]   