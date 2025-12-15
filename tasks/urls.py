from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TagListCreatView, TaskViewSet, CategoryViewSet, ExpotrtTasksView, TagListCreatView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('export-tasks/', ExpotrtTasksView.as_view(), name='export-tasks'),
    path('tags/', TagListCreatView.as_view(), name= 'tag-list-create'),

]