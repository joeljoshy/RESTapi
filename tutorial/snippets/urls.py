from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# urlpatterns = [
#     path('all',views.SnippetGeneic.as_view(),name='snippets'),
#     path('all/<int:pk>',views.Detail.as_view(),name='detail'),
#     path('users',views.UserList.as_view(),name='users'),
#     path('users/<int:pk>',views.UserDetail.as_view(),name='user_detail')
# ]

router = DefaultRouter()
router.register(r'all',views.SnippetViewSet)
router.register(r'users',views.UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
]

