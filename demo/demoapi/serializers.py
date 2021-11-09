from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User



class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ["id",'title','author','email','date']

class UserCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name','username','email','password']

    def create(self,validated_data):

            first_name = validated_data['first_name']
            username = validated_data['username']
            email = validated_data['email']
            password = validated_data['password']

            return User.objects.create_user(username=username,password=password,first_name=first_name,email=email)

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()