from django.shortcuts import render,get_object_or_404
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import response,status,serializers
from rest_framework.decorators import api_view,permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.contrib.auth import login,authenticate


# Create your views here.

#The first view should register the user and provide the serialized details
#This view will also allow group assignment.

@api_view(['POST'])
def signup(request):
    #I pass in the example of the kind of details I want the user to provide
    """
    user gets to register
    required json details include
    {
            "username":"sample",
            "email":"sample@gmail.com",
            "password":"samplepassword",
            "first_name":"samplename",
            "last_name":"samplename",
            "date_of_birth":"yyyy-mm-dd",
            "profile_picture":"link",
            "role": "student or admin"
            }
    it is a post method."""
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = get_object_or_404(CustomUser,email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        #implement an if and elif to check the different groups
        role = request.data.get('role')
        if role == 'admin':
            group1 = Group.objects.get(name='Admin')
            user.groups.add(group1)
        elif role == 'student':
            group2 = Group.objects.get(name='Student')
            user.groups.add(group2)
        else:
            raise serializers.ValidationError("Invalid role")
        return response.Response({"token":token.key,"user":serializer.data}, status=status.HTTP_201_CREATED) #we return both the token and the rest of the data
    else:
        return response.Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST) #we return a response in case of a bad request
@api_view(['POST'])
def login(request):
    """
    user gets to register
    required json details include
    {
            "email":"sample@gmail.com",
            "password":"samplepassword",
            }
    it is a post method."""
    #first, we get the user and see if they exist
    user = CustomUser.objects.get(email=request.data['email'])
    if user: #we check if user exists, if they exist
        if user.check_password(request.data['password']): #we check if the password matches
            token, created = Token.objects.get_or_create(user=user) #we get or create new token if it does not exist
                #we pass the serializer to serialize the data
            serializer = CustomUserSerializer(instance=user)
            #we return the response
            return response.Response({"token":token.key,"user":serializer.data},status=status.HTTP_200_OK)
        else: # if the password does not match
            return response.Response({"error":"incorrect details"}, status=status.HTTP_400_BAD_REQUEST)
    else: #if the user does not exist
        return response.Response({"error":"details not found"},status=status.HTTP_401_UNAUTHORIZED) 