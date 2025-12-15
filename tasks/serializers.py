
from rest_framework import serializers
from .models import Tag, Task, Category

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TagSlugRelatedField(serializers.SlugRelatedField):
    """
    Accepts tag names (strings), creates missing tags, and returns Tag instances.
    """
    def to_internal_value(self, data):
        if isinstance(data, str):
            obj, _ = Tag.objects.get_or_create(name=data)
            return obj
        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=False,
        allow_null=True,
        write_only=True
    )
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    # Accept list of tag names, create missing tags
    tags = TagSlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    title = serializers.CharField(max_length=255, help_text="The title of the task")
    description = serializers.CharField(help_text="Detailed description of the task")
    status = serializers.ChoiceField(choices=Task.choice_status, default='todo', help_text="Task status: 'todo', 'in_progress', or 'done'")

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        if tags:
            task.tags.set(tags)  # tags are Tag instances
        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance





class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']  
        ordering = ['name']  

    
