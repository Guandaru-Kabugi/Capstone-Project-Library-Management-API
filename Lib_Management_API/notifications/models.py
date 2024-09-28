from django.db import models
from Library.models import Book
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import send_mail, EmailMessage,get_connection

import ssl
User = get_user_model()

# Create your models here.
#This notification will work to send notifications to users who want to be \
    # notified when the book instance number of copies changes from 0 to 1
class BookAvailableNotification(models.Model):
    #refer to the user, who is the sender of the notification
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_notifications')
    #we then get the book as a foreign key
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_notifications')
    #we establish a way to get users to inform the management whether they want to be notified
    notified = models.BooleanField(default=False,verbose_name='Do you want to be notified?')
    
    def __str__(self):
        return f'Notification for {self.user.username} for the book {self.book.title}'
#I am working my way towards finding a solution on how users can be notified. 
#Initially, I started with this simple function that makes use of django post_save signal.
#The notified changes to True a book is checkin.
#Now the task is to find a way to create a view to get those pending notifications
def check_availability_of_books(sender,instance, created,**kwargs):
    if created == False: #We don't want a new book. We want an existing book
        if instance.number_of_copies == 1: #when the book is returned, it shifts from 0 to 1 meaning its available
            notifications = BookAvailableNotification.objects.filter(book=instance, notified=False) #we go those specific notifications
            for notification in notifications: #we make use of django send mail and an external email api company called Mailgun
                send_mail(subject=f'Notification that {notification.book.title} has been returned',
                            message='Hello! You can now log in to checkout the book.', 
                            from_email='guandarualex3@gmail.com',  
                            recipient_list=[notification.user.email], 
                            fail_silently=False,)
                notification.notified = True #when the message is sent, the notification is turned as true
                notification.save() #we save that notification on database
            
post_save.connect(receiver=check_availability_of_books,sender=Book) #we use django signals to make those updates