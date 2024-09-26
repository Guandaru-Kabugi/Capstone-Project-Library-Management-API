from django.urls import path, include
from .views import signup,login
urlpatterns = [
    path('api-auth', include('rest_framework.urls')),
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
]
