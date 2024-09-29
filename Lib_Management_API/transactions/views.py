from django.shortcuts import render,get_object_or_404
from Library.models import Book
from .models import Transaction
from .serializers import TransactionSerializer,CheckInSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,authentication_classes
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from datetime import date
User = get_user_model()
# Create your views here.
#I want to create a view that allows\
    # a student to borrow a book if the number of copies is above zero\
        # and the number of copies is deducted from existing count

#checking out a book
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class CheckOutBook(CreateAPIView):
    """
    This is a post method.
    All is needed is the id of the book and 
    the update comes automatically
    """
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all() #to allow the user to be queried from existing transactions
    def post(self,request,pk):
        #first, we get the book instance we want to borrow
        book = get_object_or_404(Book,id=pk)
        if book:
            
            #If the book exists, we check whether number of copies is above 1
            if book.number_of_copies > 0:
                
                transaction = Transaction.objects.filter(user=request.user,book=book,check_in__isnull=True).first() 
                #We need to see if user has already borrowed that specific book before
                if transaction:
                    raise serializers.ValidationError("You have already borrowed this book and not checked in yet: You can only borrow a single book")
                transaction = Transaction(
                user=request.user,
                book=book,
                
            )
                transaction.save()
                book.number_of_copies = book.number_of_copies - 1 #Here I am reducing the number of copies by 1
                book.save()
                #we accept the checkout
                serializer = TransactionSerializer(transaction)
                
                # I am serializing the transaction details
                return Response({"check_out_transaction":serializer.data,"message":"book checked out","number of remaining copies":book.number_of_copies},status=status.HTTP_200_OK) #I am returning a success message
            
            else:
                return Response({"Error":"The number of books available is 0 and cannot be checked out"},status=status.HTTP_404_NOT_FOUND) #error handling when number of books is inadequate

"""we create a view that allows us to list all available books whose number of copies is above 0
We now implement a way for user to return the borrowed book"""

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class CheckInBook(CreateAPIView):
    """
    This is a post method. Does not take any input, just the id of the book and
    it will automatically make the necessary changes
    """
    serializer_class = TransactionSerializer #we obtained the serialized data
    #we pass the query
    queryset = Transaction.objects.all()
    #we then override the post method
    def post(self, request, pk):
        #We first get the book that they student wants to return
        book = get_object_or_404(Book,id=pk)
        #we confirm if the book exists
        if book:
            #we check if user has borrowed that book
            # transaction = get_object_or_404(Transaction,user=request.user,book=book)
            transaction = Transaction.objects.filter(user=request.user,book=book,check_in__isnull=True).first()    
            #We return the book
            if transaction:
                transaction.check_in = date.today()
                transaction.save()
                book.number_of_copies = book.number_of_copies + 1 #we return the book
                book.save() #we save the instance of the book returned
                serializer = CheckInSerializer(transaction)
                return Response({"check_in_transaction":serializer.data,"message":"book checked in","number of remaining copies":book.number_of_copies},status=status.HTTP_200_OK)
            else:
                return Response({"Error":"You do not have any book checked out or you have checked in already"}, status=status.HTTP_400_BAD_REQUEST)
    
#we now work on generating all transactions belonging to that user
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,SessionAuthentication,BasicAuthentication])
class ListTransactions(ListAPIView):
    """
    Provides a list of all the transactions the user has.
    It represents the books they have checked in or out
    User must be authenticated and can only see their transactions
    It is a get method
    """
    serializer_class = CheckInSerializer
    def get_queryset(self):
        user = self.request.user
        return user.user_transactions.all()
    