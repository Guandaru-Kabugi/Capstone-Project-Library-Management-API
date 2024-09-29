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
            "number_of_copies":1,
            "edition":"1st Ed",
            "database":database_id
            
        })
        self.client.logout()
        self.client.login(email='lawrence@gmail.com',password='Lawrencelx123.')
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_out_url = reverse('checkout',args=[book.id])
        self.client.post(self.check_out_url)
        self.client.logout
    #Test checkout--------------------------------------
    #--------------------------------------------------
    #-------------------------------------------------
    #We now test checking out of the book
    def test_student_to_be_notified_book_return(self):
        # we login a new user 
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f'Token to test student checkout of book {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        book = Book.objects.get(title='yes yes yes')
        print(f'we confirm if number of books remaining is zero {book.number_of_copies}')
        self.subscribe_to_notifications_urls = reverse('subscribe',args=[book.id])
        response = self.client.post(self.subscribe_to_notifications_urls)
        print(f'response data after notification activation {response.data}')
        #I want to check If the notified is false
        user = User.objects.get(username='James')
        self.pending_url = reverse('pending')
        response = self.client.get(self.pending_url)
        # print(f"checking notifications {response.data}")
    def test_available_books(self):
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f'Token to test student checkout of book {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.available_books_url = reverse('available_books')
        response = self.client.get(self.available_books_url)
        print(f'testing whether available books are shown {response.data}')