from django.shortcuts import render,get_object_or_404
from .models import BookAvailableNotification
from .serializers import NotifyBookAvailableSerializer
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import permission_classes,authentication_classes
from Library.models import Book
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication

# Create your views here.


#we create a view so that a user can go to that specific book to activate the notification
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class CreateNotificationOnAvailableBooks(CreateAPIView):
    """"
    
    This is a post request.
    The user gets to subscribe so that a notification is sent if they are interested in
    learning more about the book.
    once they click post, a notification gets created in the database
    """
    serializer_class = NotifyBookAvailableSerializer
    queryset = BookAvailableNotification.objects.all()

    def post(self, request, pk):
        #we must get the book that the user wants to be notified about
        book = get_object_or_404(Book,id=pk)
        if book:
            #we filter to ensure that a similar notification does not exist
            notifications = BookAvailableNotification.objects.filter(user=request.user,book=book,notified=False)
            if notifications:
                raise serializers.ValidationError("You cannot subscribe twice. A subscription already exists.")
            #I create new notification for the user 
            notification = BookAvailableNotification(
                book = book,
                user = request.user
            )
            #we save it
            notification.save()
            #we serialize it
            serializer = NotifyBookAvailableSerializer(notification)
            #we return a response
            return Response({"user":serializer.data}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({"Error":"Book unavailable"}, status=status.HTTP_404_NOT_FOUND)
        
#view pending notifications
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class ListPendingNotifications(ListAPIView):
    """
    This is a get method
    The result has been filtered
    it is filtered to only send back notifications where book has not been checked in
    once a book is checked in, the notification disappears.
    Only authenticated users can access.
    """
    serializer_class = NotifyBookAvailableSerializer
    def get_queryset(self):
        user = self.request.user
        return user.user_notifications.filter(notified=False)
        