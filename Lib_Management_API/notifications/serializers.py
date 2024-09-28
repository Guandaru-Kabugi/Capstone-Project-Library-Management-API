from rest_framework import serializers
from .models import BookAvailableNotification

class NotifyBookAvailableSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title',read_only=True)
    book_author = serializers.CharField(source='book.author',read_only=True)
    class Meta:
        model = BookAvailableNotification
        fields = ['id','book','book_title','book_author']