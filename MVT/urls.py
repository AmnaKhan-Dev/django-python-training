from rest_framework import routers
from django.urls import path, include
from .views import AuthorViewSet, AuthorBioViewSet, GenreViewSet, BooksViewSet, author_list_view

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'author-bios', AuthorBioViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),  # all DRF endpoints
    path('authors-template/', author_list_view, name='authors_list'),  #template view
]