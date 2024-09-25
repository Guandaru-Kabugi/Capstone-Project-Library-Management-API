from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

#We now need to create a serializer that will serialize user data when they register or login
class CustomUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','token','first_name','last_name', 'date_of_membership','active_status','email','username','role','profile_image']
