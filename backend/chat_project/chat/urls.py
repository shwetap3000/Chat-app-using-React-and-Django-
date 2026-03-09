from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('conversation/create/', views.create_conversation),
    path('conversations/<int:user_id>/', views.get_conversations),
    path('messages/<int:conversation_id>/', views.get_messages),
]
