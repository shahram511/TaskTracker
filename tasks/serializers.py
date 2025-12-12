from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category',required=False,allow_null=True, write_only=True)
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    title = serializers.CharField(
        max_length=255,
        help_text="The title of the task"
    )
    description = serializers.CharField(
        help_text="Detailed description of the task"
    )
    status = serializers.ChoiceField(
        choices=Task.choice_status,
        default='todo',
        help_text="Task status: 'todo', 'in_progress', or 'done'"
    )
    def validate_category_id(self, value):
        user = self.context['request'].user
        if value and value.owner != user:
            raise serializers.ValidationError("You are not allowed to assign this category to this task")
        return value
    
