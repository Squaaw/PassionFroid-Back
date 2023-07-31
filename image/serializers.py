from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'description', 'base64', 'width', 'height', 'vector', 'created_at', 'updated_at')