from .models import Blog
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'desc']


    # title = serializers.CharField(max_length=200)
    # desc = serializers.CharField(max_length=500)
    #
    # def create(self, validated_data):
    #     return Blog.objects.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.desc = validated_data.get('desc', instance.desc)
    #     instance.save()
    #     return instance