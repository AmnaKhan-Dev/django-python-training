from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, AuthorBio, Genre, Books
from .serializers import AuthorSerializer, AuthorBioSerializer, GenreSerializer, BooksSerializer


# It is a Django REST Framework (DRF) class that provides all the common actions: list, retrieve, create, update, partial_update, destroy.
# Think of it as a “ready-made CRUD view” for your model.
# You don’t have to write separate functions for GET/POST/PUT/DELETE unless you want custom behavior.

class AuthorViewSet(viewsets.ModelViewSet):#viewset is a class that provides the basic functionality for views
    queryset = Author.objects.all() #this is the queryset that will be used to get the data
    serializer_class = AuthorSerializer #validate request data and convert the data to JSON

class AuthorBioViewSet(viewsets.ModelViewSet):
    queryset = AuthorBio.objects.all()
    serializer_class = AuthorBioSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
# Create your views here.


def author_list_view(request): #This function is a normal Django view that renders a template and passes the data to it
    authors = Author.objects.all()  #Get data from the database
    return render(request, "authors/author_list.html", {"authors": authors}) 
    #Render the template and pass the data to it Tells Django to use the authors/author_list.html file.
    #Passes the authors queryset to the template as a variable named authors.

