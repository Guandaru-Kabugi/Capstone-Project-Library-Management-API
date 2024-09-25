from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from rest_framework import status, response
from django.contrib.auth.models import Group
# Create your tests here.

class TestViews(APITestCase):
    def setUp(self):
        #this method sets up some of the common attributes that will be needed for the rest of the tests
        self.client = APIClient()
        self.signup_url = reverse('signup') #allows me to access the signup url as if I was using browsable api
        self.login_url = reverse('login') # allows me to access login url as if I was using browsable api
        Group.objects.create(name='Admin') #I am creating groups that resemble the actual groups in database
        Group.objects.create(name='Student') #I am creating groups that resemble the actual groups in database
        self.new_user = self.client.post(self.signup_url,{
            "username":"James",
            "email":"james@gmail.com",
            "password":"Jameslx123.",
            "first_name":"James",
            "last_name":"Johnson",
            "date_of_birth":"2000-11-11",
            "profile_image":"",
            "role": "student",
            "active_status":True
        })
    def test_signup_new_useradmin(self):
        #here, we simply check whether we are able to signup the user and get the intended response data and status code
        #WE FIRST TEST WHETHER THE ADMIN ROLE IS BEING ADDED EFFECTIVELY
        response = self.client.post(self.signup_url,{
            "username":"Michael",
            "email":"michael@gmail.com",
            "password":"Michaelalx123.",
            "first_name":"Michael",
            "last_name":"Maina",
            "date_of_birth":"2000-11-11",
            "profile_image":"",
            "role": "admin",
            "active_status":True
        })
        #HERE, I USED PRINT STATEMENT TO TEST WHETHER GROUPS WERE CREATED CORRECTLY
        groups = Group.objects.all()
        print(groups)
        #I PRINTED TO CHECK THE DATA CONTENT TO SEE IF THE TOKEN AND ALSO THE ROLE WERE PRESENT
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data['user']) #I WANTED TO CHECK INDIVIDUAL DATA
        self.assertEquals(response.data['user']['username'],'Michael')
    def test_signup_new_userstudent(self):
        #HERE, I AM CHECKING IMPLEMENTATION OF STUDENT ROLE
        response = self.client.post(self.signup_url,{
            "username":"Ann",
            "email":"ann@gmail.com",
            "password":"Annalx123.",
            "first_name":"Ann",
            "last_name":"Annita",
            "date_of_birth":"2000-11-11",
            "profile_image":"",
            "role": "student",
            "active_status":True
        })
        #HERE, I USED PRINT STATEMENT TO TEST WHETHER GROUPS WERE CREATED CORRECTLY
        groups = Group.objects.all()
        print(groups)
        #I PRINTED TO CHECK THE DATA CONTENT TO SEE IF THE TOKEN AND ALSO THE ROLE WERE PRESENT
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data['user']) #I WANTED TO CHECK INDIVIDUAL DATA
        self.assertEquals(response.data['user']['username'],'Ann')
    def test_login_new_user(self):
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f"James's token after login: {token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        print(f"Response data for james after login: {response.data}")