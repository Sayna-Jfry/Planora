from rest_framework import serializers
from .models import ProjectModel

class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = '__all__'
        read_only_fields = ['created_at', 'creator']


