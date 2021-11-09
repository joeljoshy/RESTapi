from rest_framework import serializers
from .models import Todo
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class TodoSerializer(ModelSerializer):
    class Meta:

        model = Todo
        fields = ["id","task_name","status","user"]

class UserCreationSerializer(ModelSerializer):

    class Meta:

        model = User
        fields = ["first_name","username","email","password"]

    def create(self, validated_data):
        first_name = validated_data['first_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        return User.objects.create_user(username=username,email=email,first_name=first_name,password=password)



class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()