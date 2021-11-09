from django.shortcuts import render
from rest_framework.response import Response
from .serializers import SnippetSerializer,UserSerializer
from .models import Snippet
from rest_framework import status, renderers
from rest_framework.views import APIView
from rest_framework import mixins,generics,viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action

# Create your views here.


class SnippetAPIView(APIView):

    def get(self,request):

        snippets = Snippet.objects.all()
        serializer= SnippetSerializer(snippets,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):

        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SnippetGeneic(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):

    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class SnippetDetail(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):

    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class Detail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self,request,*args,**kwargs):

        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
