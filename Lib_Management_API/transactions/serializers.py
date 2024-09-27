from rest_framework import serializers
from .models import Transaction
from datetime import date


class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','user','username','book','book_title']
    # Override the create method to handle user and book directly
#since the details we want for the check_in are more than those of checkout, \
    # we create another serializer
class CheckInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    check_out = serializers.DateField(read_only=True)
    penalty_fees = serializers.DecimalField(read_only=True,max_digits=6,decimal_places=2)
    check_in = serializers.DateField(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','user','username','book','book_title','check_out','penalty_fees','check_in']