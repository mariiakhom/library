from rest_framework import serializers

from .models import *


class BookSerializer1(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover']


class BookSerializer2(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    genres = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover', 'genres']

