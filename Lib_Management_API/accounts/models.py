from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

#HERE WILL BE THE USER MANAGER METHOD
class UserManager(BaseUserManager):
    def create_user(self,email,username,first_name,last_name,password):
        #first we check and ensure that user provide required registration details
        if not email:
            raise ValueError("You must provide an email.")
        if not username:
            raise ValueError("You must provide a username")
        if not first_name:
            raise ValueError("You must provide your first name")
        if not last_name:
            raise ValueError("You must provide your last name")
        user = self.model(email=self.normalize_email(email),username=username,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,first_name,last_name,password):
        user = self.create_user(email=self.normalize_email(email),username=username,first_name=first_name,last_name=last_name,password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
# HERE WILL BE THE ABTRACT USER INHERITANCE TO MY CUSTOMERUSER MODEL
class CustomUser(AbstractUser):
    ROLES = [
        ('student','Student'),
        ('admin','Admin'),
    ]
    #The user should have unique email, username, date of membership, and active status
    email = models.EmailField(unique=True,verbose_name='User Email',max_length=200,null=False)
    username = models.CharField(unique=True,verbose_name='username',max_length=50,null=False)
    date_of_membership = models.DateTimeField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    first_name = models.CharField(unique=False,null=False,max_length=100,verbose_name='User First Name')
    last_name = models.CharField(unique=False,null=False,max_length=100,verbose_name='User Last Name')
    profile_image = models.URLField(blank=True,null=True,max_length=240,verbose_name='provide a url link to your profile image')
    role = models.CharField(max_length=20,choices=ROLES, default='student')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = UserManager() #here, we are focusing on referencing the usermanager that will handle authentication.
    
    def __str__(self):#we want to return the username whenever the user instance is required.
        return self.username
    

