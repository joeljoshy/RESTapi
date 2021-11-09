from django.urls import path
from . import views

urlpatterns = [
    path('todos',views.TodoList.as_view(),name='todos'),
    path('todos/<int:pk>',views.TodoDetailView.as_view(),name='todo_detail'),
    path('accounts/signup',views.UserCreationView.as_view(),name='register'),
    path('accounts/signin',views.LoginView.as_view(),name='signin')
]


# token johny123: 8d5a6952cce084a862df02b0544fdef0f69ede93

# johny:8298730321ae7745805f135e21db20fded5c868d