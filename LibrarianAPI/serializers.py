from rest_framework import serializers
from .models import Books, BorrowRequest, BorrowRequestHistory, LibraryUser


class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ['id', 'name', 'email', 'password']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['book_id', 'title', 'author', 'description']


class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['id', 'user', 'book', 'start_date', 'end_date', 'status']


class BorrowRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequestHistory
        fields = ['id', 'user', 'book', 'action', 'start_date', 'end_date']
