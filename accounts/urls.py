from .views import UserCreate
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'

urlpatterns = [
    path('create_user/', UserCreate.as_view(), name="create_user"),
    path('login/', LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
