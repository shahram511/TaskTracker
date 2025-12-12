from django.db.models import When, Case, IntegerField

from rest_framework import viewsets, filters
from rest_framework.response import Response
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import action
from drf_spectacular.types import OpenApiTypes

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Category management.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoints for Task management.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    # Remove filters.OrderingFilter to prevent it from overwriting custom ordering
    filter_backends = [
        DjangoFilterBackend,       # for exact filtering
        filters.SearchFilter,      # for searching
    ]
    
    filterset_fields = ['status', 'priority', 'category']  # for exact filtering
    search_fields = ['title', 'description']   # for searching

    # Documentation for GET (List)
    @extend_schema(
        
        parameters=[
            OpenApiParameter(
                name='ordering',
                description='Which field to use when ordering the results. (e.g. priority, -priority, created_at)',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='status',
                description='Filter by task status',
                required=False,
                type=str,
                enum=['todo', 'in_progress', 'done']
            ),
            OpenApiParameter(
                name='priority',
                description='Filter by task priority',
                required=False,
                type=str,
                enum=['low', 'medium', 'high']
            ),
            OpenApiParameter(
                name='category',
                description='Filter by task category id',
                required=False,
                type=int,
            ),
        ]
        
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get statistics of user's tasks",
        description="retrieve statistics data about the user's tasks",
        responses={
            200: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                name="Successful Response",
                value={
                    "total_tasks": 10,
                    "status_counts": {
                        "todo": 5,
                        "in_progress": 3,
                        "done": 2,
                    },
                    "priority_counts": {
                        "low": 3,
                        "medium": 4,
                        "high": 3,
                    },
                },
            ),
        ],
    )
    @action(detail=False, methods=['get'])
    def statistics(self,request):
        """
        Get statistics of user's tasks
        """
        user_tasks=Task.objects.filter(owner=request.user)
        data={
            'total_tasks': user_tasks.count(),
            "status_counts": {
                "todo": user_tasks.filter(status="todo").count(),
                "in_progress": user_tasks.filter(status="in_progress").count(),
                "done": user_tasks.filter(status="done").count(),
            },
            "priority_counts": {
                "low": user_tasks.filter(priority="low").count(),
                "medium": user_tasks.filter(priority="medium").count(),
                "high": user_tasks.filter(priority="high").count(),
            },
        }
        return Response(data)

    @action(detail=True, methods=['post'],url_path= 'complete')
    def mark_as_done(self,request,pk=None):
        """
        Mark a task as done
        """
        task=self.get_object()
        task.status="done"
        task.save()
        return Response({'message': 'Task marked as done'})
    
    def get_queryset(self):
        # 1. Base queryset
        queryset = Task.objects.filter(owner=self.request.user)
        
        # 2. Get ordering parameter manually
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        # 3. Apply ordering logic
        if 'priority' in ordering:
            # Add custom priority sorting value
            queryset = queryset.annotate(
                priority_val=Case(
                    When(priority='low', then=1),
                    When(priority='medium', then=2),
                    When(priority='high', then=3),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            
            # Check for descending order
            if ordering.startswith('-'):
                queryset = queryset.order_by('-priority_val', '-created_at')
            else:
                queryset = queryset.order_by('priority_val', '-created_at')
                
        else:
            # Standard ordering for other fields
            queryset = queryset.order_by(ordering)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)