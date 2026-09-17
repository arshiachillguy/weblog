from rest_framework import serializers
from .models import post

class PostSerializer(serializers.ModelSerializer):
     author = serializers.StringRelatedField()
     class Meta:
          model = post
          fields = '__all__'
          #just for showing - user can't sent it on the req
          read_only_fields = ['author']