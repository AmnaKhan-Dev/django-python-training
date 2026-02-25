from rest_framework import serializers
from .models import Author, AuthorBio, Genre, Books

class AuthorSerializer(serializers.ModelSerializer):#this is a serializer for the Author model
    class Meta: # nested class that defines the model and fields that will be serialized
        model = Author #this is the model that will be serialized
        fields = '__all__' #this is the fields that will be serialized

class AuthorBioSerializer(serializers.ModelSerializer):#
    class Meta:
        model = AuthorBio
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)