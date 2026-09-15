from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    
    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        return user


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
     
    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        instance.username = validated_data.get(
            'username',
            instance.username
        )

        instance.email = validated_data.get(
            'email',
            instance.email
        )

        if password:
            instance.set_password(password)

        instance.save()

        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:    
        model = User
    
        fields = ['id', 'username', 'email']