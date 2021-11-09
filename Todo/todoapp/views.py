from django.shortcuts import render
from rest_framework.views import APIView
from .models import Todo
from .serializers import TodoSerializer,UserCreationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins,generics,permissions,authentication

from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
# Create your views here.

class Todos(APIView):

    def get(self,request):

        todos = Todo.objects.all()
        serializer = TodoSerializer(todos,many=True) #for more than one objects
        return Response(serializer.data)
    def post(self,requset):

        serializer = TodoSerializer(data=requset.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#put , delete

class TodoDetails(APIView):
    def get_object(self,pk):
        try:
            return Todo.objects.get(id=pk)
        except Todo.DoesNotExist:
            raise Http404

    def get(self,request,**kwargs):

        todo = self.get_object(kwargs['pk'])
        serializer = TodoSerializer(todo)

        return Response(serializer.data)

    def put(self,request,**kwargs):

        todo = self.get_object(kwargs['pk'])
        serializer = TodoSerializer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,**kwargs):

        todo = self.get_object(kwargs['pk'])
        todo.delete()
        return Response({'message':'deleted'})

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

class TodoList(generics.GenericAPIView,
               mixins.ListModelMixin,
               mixins.CreateModelMixin):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    authentication_classes = [
        # authentication.BasicAuthentication,
        # authentication.SessionAuthentication
        authentication.TokenAuthentication
    ]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user)
        return todos

    def get(self,request,*args,**kwargs):
        print(request.user)
        return self.list(request,*args,**kwargs)

    def perform_create(self, serializer): #to add current user to model
        user = self.request.user
        serializer.save(user=user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class TodoDetailView(generics.GenericAPIView,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    # def perform_update(self, serializer): #to override update
    #     serializer.save()

    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
