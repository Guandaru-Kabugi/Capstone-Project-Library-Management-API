from django.urls import path
from .views import CheckOutBook,CheckInBook
urlpatterns = [
    path('available_books/checkout/<int:pk>/',CheckOutBook.as_view(),name='checkout'),
    path('available_books/checkin/<int:pk>/',CheckInBook.as_view(),name='checkin'),
]
