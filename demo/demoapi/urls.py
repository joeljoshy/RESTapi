from django.urls import path
from .views import ArticleAPIView,ArticleDetails,GenericAPIView,DetailGeneric,LoginView,UserCreationView,PostListCreateView



urlpatterns = [

    path('article',GenericAPIView.as_view(),name='articles'),
    path('article-list', PostListCreateView.as_view(), name='articles'),
    path('article/<int:pk>',DetailGeneric.as_view(),name="article_detail"),
    path('accounts/signup',UserCreationView.as_view(),name='signup'),
    path('accounts/signin',LoginView.as_view(),name='signin')
]



# token johny1 : 9dd7683e99b1ab585257fbc672bfddd42f9a98b8
# joel123 : e91cd7cd8606ea5dbc961f7f3a4de0ecb6fba1bd