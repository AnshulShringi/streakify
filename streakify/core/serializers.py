from rest_framework import serializers
from streakify.core.models import ImageModel 


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['image',]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None