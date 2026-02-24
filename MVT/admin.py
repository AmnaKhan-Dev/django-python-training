from django.contrib import admin

# Register your models here.
from .models import Author, AuthorBio, Genre, Books

admin.site.register(Author)
admin.site.register(AuthorBio)
admin.site.register(Genre)
admin.site.register(Books)