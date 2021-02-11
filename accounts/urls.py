from django.urls import path 
from rest_framework.authtoken.views import ObtainAuthToken


app_name = 'accounts'

urlpatterns = [
    path('auth/', ObtainAuthToken.as_view(), name='auth'),
]