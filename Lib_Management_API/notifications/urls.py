from django.urls import path
from .views import CreateNotificationOnAvailableBooks,ListPendingNotifications

urlpatterns = [
    path('recieve/notifications/<int:pk>/',CreateNotificationOnAvailableBooks.as_view(),name='subscribe'),
    path('list/pending/notifications/',ListPendingNotifications.as_view(),name='pending'),
]
