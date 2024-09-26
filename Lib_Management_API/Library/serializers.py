from rest_framework import serializers
from .models import Book,Database


#We create a databaseserializer that allows us to create necessary databases to the project database
class DatabaseSerializer(serializers.ModelSerializer):
    #I want to return the number of books within the database when created or accessed
    number_of_books_in_database = serializers.SerializerMethodField() #helps add the attribute into the serializer
    class Meta:
        model = Database
        fields = ['id','database_name','number_of_books_in_database']
    def get_number_of_books_in_database(self,obj): #gets the attribute used under property method
        return obj.books_in_database #we return the attribute 
#we create a BookSerializer to allow us to add, edit, delete, or update a book instance
class BookSerializer(serializers.ModelSerializer):
    database_name = serializers.CharField(source='database.database_name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id','title','isbn','author','database_name','database','published_date','number_of_copies','edition']
    
