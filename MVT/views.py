from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, AuthorBio, Genre, Books
from .serializers import AuthorSerializer, AuthorBioSerializer, GenreSerializer, BooksSerializer

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import render
from .forms import ContactForm


import logging

logger = logging.getLogger(__name__) #This is a logger object that will be used to log messages to the console
logger.info("Login attempt")

# • APIView is more low-level; it doesn’t know anything about models automatically.
# • You manually define methods for HTTP verbs:
# get(self, request) → handle GET
# post(self, request) → handle POST
# put(self, request) → handle PUT
# delete(self, request) → handle DELETE


class SignupAPIView(APIView):
    def post(self, request): #
        username = request.data.get('username')
        password = request.data.get('password')

        logger.info(f"Login attempt for username: {username}")

        if not username or not password:
            return Response({"error": "Username and password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists(): #check if the username already exists
            return Response({"error": "Username already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create the user
        user = User.objects.create(
            username=username,
            password=make_password(password)  # encrypt the password
        )

        return Response({"message": "User created successfully", "username": user.username},
                        status=status.HTTP_201_CREATED)

# API login view
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data) #LoginSerializer is a serializer for the Login model   
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username'] #username is the username of the user
        password = serializer.validated_data['password'] #password is the password of the user

        logger.info(f"Login attempt for username: {username}")

        user = authenticate(username=username, password=password) #authenticate is a function that authenticates the user
        if user:
            # generate JWT tokens: This is a way to generate a token that can be used to authenticate the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED) #if the user is not authenticated, return an error message

# It is a Django REST Framework (DRF) class that provides all the common actions: list, retrieve, create, update, partial_update, destroy.
# Think of it as a “ready-made CRUD view” for your model.
# You don’t have to write separate functions for GET/POST/PUT/DELETE unless you want custom behavior.

class AuthorViewSet(viewsets.ModelViewSet):#viewset is a class that provides the basic functionality for views - viewsets are a way to create a view for a model
    queryset = Author.objects.all() #this is the queryset that will be used to get the data
    serializer_class = AuthorSerializer #validate request data and convert the data to JSON
    #permission_classes = [IsAuthenticated]  # only logged-in users can access
class AuthorBioViewSet(viewsets.ModelViewSet):
    queryset = AuthorBio.objects.all()
    serializer_class = AuthorBioSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.select_related('author').prefetch_related('genres')
    serializer_class = BooksSerializer
# Create your views here.


def author_list_view(request): #This function is a normal Django view that renders a template and passes the data to it
    authors = Author.objects.all()  #Get data from the database
    return render(request, "authors/author_list.html", {"authors": authors}) 
    #Render the template and pass the data to it Tells Django to use the authors/author_list.html file.
    #Passes the authors queryset to the template as a variable named authors.

def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)  # validated data
    return render(request, "contact.html", {"form": form})