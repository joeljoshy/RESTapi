from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from .serializers import ArticleSerializer,UserCreationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login,logout,authenticate
from rest_framework import generics,mixins,authentication,permissions
from rest_framework.authtoken.models import Token
# Create your views here.

class UserCreationView(APIView):

    def post(self,request):

        serializer = UserCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                token,created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key,'msg':'login successful '})
            else:
                return Response({'msg':'Invalid credentials'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GenericAPIView(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     ):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    authentication_classes = [
        # authentication.BasicAuthentication,
        # authentication.SessionAuthentication
        authentication.TokenAuthentication
    ]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        articles = Article.objects.filter(author=self.request.user)
        return articles

    def get(self,request,*args,**kwargs):
        print(request.user)
        return self.list(request,*args,**kwargs)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
    def post(self,request):

        return self.create(request)

class DetailGeneric(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    permission_classes = [
        permissions.IsAuthenticated
    ]
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def get_queryset(self):
        articles = Article.objects.filter(author=self.request.user)
        return articles

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class PostListCreateView(generics.ListCreateAPIView):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


    def get_queryset(self):
        articles = Article.objects.filter(author=self.request.user)
        return articles









class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self,request):

        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetails(APIView):

    def get_object(self,id):
        try:
            return Article.objects.get(id=id)

        except Article.DoesNotExist:

            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):

        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)