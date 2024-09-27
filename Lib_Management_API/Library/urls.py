from django.urls import path, include
from .views import BookView,DatabaseView,BookList
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(r'database',DatabaseView,basename='database')
router.register(r'books',BookView,basename='books')

urlpatterns = [
    path('',include(router.urls)),
    path('available_books/',BookList.as_view(),name='available_books'), #First path to checkout books
]
