from django.test import TestCase
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient,APITestCase
from Library.models import Book,Database
from .models import Transaction
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import Group
# Create your tests here.

class TestViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        #Since I have already tested creation of books, here the goal is checkout.
        #I will create a few book instances in this setUp
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
    def test_checkout_book_student(self):
        #we login to get the token
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f'Token to test student checkout of book {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #After we login in, the next step is to now checkout
        #we get the specific book
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_out_url = reverse('checkout',args=[book.id])
        response = self.client.post(self.check_out_url)
        print(f"testing book checkout data by student{response.data}")
    def test_checkin_book_student(self):
        #we login to get the token
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f'Token to test student checkout and in of book {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #After we login in, the next step is to now checkout
        #we get the specific book
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_out_url = reverse('checkout',args=[book.id])
        response = self.client.post(self.check_out_url)
        print(f"testing book checkout data by student{response.data}")
        
        #we then check in
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_in_url = reverse('checkin',args=[book.id])
        response = self.client.post(self.check_in_url)
        print(f"testing book checkin data by student{response.data}")
    def test_list_all_transactions(self):
        #we login to get the token
        response = self.client.post(self.login_url,{
            "email":"james@gmail.com",
            "password":"Jameslx123."
        })
        token = response.data.get('token')
        print(f'Token to test student checkout and in of book {token}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        #After we login in, the next step is to now checkout
        #we get the specific book
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_out_url = reverse('checkout',args=[book.id])
        response = self.client.post(self.check_out_url)
        print(f"testing book checkout data by student{response.data}")
        
        #we then check in
        book = Book.objects.get(title='yes yes yes')
        user = User.objects.get(username='James')
        self.check_in_url = reverse('checkin',args=[book.id])
        response = self.client.post(self.check_in_url)
        print(f"testing book checkin data by student{response.data}")
        
        #we print out all transactions
        
        self.list_transactions_url = reverse('alltransactions')
        response = self.client.get(self.list_transactions_url)
        print(f'Results for all user transactions {response.data}')