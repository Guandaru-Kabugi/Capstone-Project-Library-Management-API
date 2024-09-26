from django.urls import path, include
from .views import BookView,DatabaseView
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(r'database',DatabaseView,basename='database')
router.register(r'books',BookView,basename='books')

urlpatterns = [
    path('',include(router.urls)),
]
