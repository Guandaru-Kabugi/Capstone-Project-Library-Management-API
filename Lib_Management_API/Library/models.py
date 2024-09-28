from django.db import models

from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

#I need a model for book and database
#This model will work like the real library which usually\
    # have different databases that store books from different disciplines
class Database(models.Model):
    database_name = models.CharField(max_length=100,verbose_name='Database',null=False,unique=True)
     #Here I want to makes books_in_database behave like an attribute instead of a method,
        #so you can access it as as a normal attribute like the rest of the attributes.
    @property
    def books_in_database(self):
        number_of_books_in_database = self.books.all().count()
        return str(number_of_books_in_database)
    def __str__(self):
        return self.database_name
class Book(models.Model):
    title = models.CharField(max_length=150,verbose_name='book title',null=False,unique=False)
    author = models.CharField(max_length=100, verbose_name='Author(s)',help_text='For more than 1 author, separate names with a comma',null=False)
    isbn = models.CharField(verbose_name='ISBN',max_length=13,unique=True,null=False)
    published_date = models.DateField(verbose_name='Publication_Date')
    number_of_copies =models.PositiveIntegerField(verbose_name='Number of Copies Available')
    edition = models.CharField(max_length=10,verbose_name='Book Edition')
    database = models.ForeignKey(Database,on_delete=models.CASCADE,related_name='books')
    
    def __str__(self):
        return f'Author(s):{self.author}, Title: {self.title}.'
    #Since I created Group admin and student, I want the add to have all crud operations, while student can only read or borrow
    class Meta:
        permissions = [
            ('create', 'can add a new book'),
            ('edit', 'can update an existing book'),
            ('delete', 'can delete an existing book')
        ]

