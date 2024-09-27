from typing import Iterable
from django.db import models
from Library.models import Book
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
User = get_user_model()
# Create your models here.

#I am thinking that creating a transaction model to handle transactions is the best approach

class Transaction(models.Model):
    FEE_CHARGED_PER_DAY = 50.00 #This is in KES or Kenyan Shillings
    #This model will represent a single transaction
    #here, I am referencing the User created, who will be the student
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_transactions')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='book_transactions')
    #here I focus on checkin and checkout
    check_out = models.DateField(verbose_name='date of check_out of book', auto_now_add=True)
    check_in = models.DateField(verbose_name='date of  check_in of book',null=True,blank=True)
    #Here I focus on tracking lateness and implementing any applicable fees
    number_of_days_late = models.PositiveIntegerField(verbose_name='Tracks number of days book is late for return',default=0)
    late = models.BooleanField(default=False,verbose_name='Whether book is late for return or not')
    returned = models.BooleanField(default=False, verbose_name='Whether the book has been returned')
    due_date = models.DateField(verbose_name='date when the book is due', null=True, blank=True)
    penalty_fees = models.DecimalField(max_digits=6,decimal_places=2, null=True, blank=True)
    late_days = models.PositiveIntegerField(default=0, verbose_name='number of days late')
    #as per django models, there is a save method that can be overriden to make these changes automatically
    
    def save(self, **kwargs):
        if not self.pk:  # Check if the instance is being created
            self.check_out = self.check_out or timezone.now().date()  # Ensure check_out is set
        #I want to update the return date of the book automatically to 30 days after checkout
        if self.check_out and self.due_date is None:
            print(f"Saving Transaction: Book,{self.book.title} borrowed by {self.user.username} on {self.check_out}")
            self.due_date = self.check_out + timedelta(days=30) #I use timedelta because it is able to add or subtract between two time objects
            print(f"Due date set to: {self.due_date}")
        #we check whether self.checkin and self.duedate are present
        if self.check_in and self.due_date:
            #we get the number of days late
            number_of_late_days = (self.check_in - self.due_date).days #Here I want to update the late_days automatically
            if self.late_days>0: #I want to check whether the number of days late is greater than Zero
                self.late = True #I automatically update that the book is late for return; True
                #we then get the penalty
                self.late_days = number_of_late_days #I update the late days
                self.penalty_fees = number_of_late_days * self.FEE_CHARGED_PER_DAY #I update the penalty of fees
            else:
                #I ensure that The rest remains default
                self.late = False
                self.late_days = 0
                self.penalty_fees = 0.00
            #here I acknowledge the book has been returned
            self.returned = True
        else:
            #If check_in not present
            self.returned = False
            self.penalty_fees = None #I only charge when the book is returned
                
        super().save(**kwargs) # Call the "real" save() method
    def __str__(self):
        return f'Student {self.user.username} borrowed {self.book.title} on {self.check_out}'
    
    
