from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from notifications.models import BookAvailableNotification
from django.contrib.auth import get_user_model
User = get_user_model()
from Library.models import Book, Database
# Create your tests here.

class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.subscribe_to_notifications_urls = reverse('subscribe')
        admin_group = Group.objects.create(name='Admin') #I am creating groups that resemble the actual groups in database
        student_group = Group.objects.create(name='Student') #I am creating groups that resemble the actual groups in database
        self.database_url = reverse('database-list') #list is added to perform operates like list, delete, update, create
        self.books_url = reverse('books-list')
        
        self.signup_url = reverse('signup') #allows me to access the signup url as if I was using browsable api
        self.login_url = reverse('login') # allows me to access login url as if I was using browsable api
        #we set up two students for testing
        self.newstudent_user = self.client.post(self.signup_url,{
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
        self.newstudent2_user = self.client.post(self.signup_url,{
            "username":"Lawrence",
            "email":"lawrence@gmail.com",
            "password":"Lawrencelx123.",
            "first_name":"Lawrence",
            "last_name":"Jonana",
            "date_of_birth":"2000-11-11",
            "profile_image":"",
            "role": "student",
            "active_status":True
        })
        #superuser to create database
        self.superuser = User.objects.create_superuser(
            username='Maina',
            email='mainawes@gmail.com',
            password='Mainaalxes123.',
            first_name = 'Maina',
            last_name = 'John'
            
        )
        #the superuser creates the databases
        self.client.login(email='mainawes@gmail.com',password=('Mainaalxes123.'))
        self.client.post(self.database_url,{
            'database_name':'Literature'
        })
        self.client.post(self.database_url,{
            'database_name':'History'
        })
        database = Database.objects.get(database_name='History')
        database_id = database.id
        #first book is created
        self.client.post(self.books_url,{
            "title":"yes yes yes",
            "author":"James,John",
            "isbn":"8791762769716",
            "published_date":"2011-11-11",
            "number_of_copies":5,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.client.logout()
    #Test checkout--------------------------------------
    #--------------------------------------------------
    #-------------------------------------------------
    #We now test checking out of the book
        
        