from rest_framework import routers
from django.urls import path, include
from .views import AuthorViewSet, AuthorBioViewSet, GenreViewSet, BooksViewSet, author_list_view , LoginAPIView,SignupAPIView, contact_view

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'author-bios', AuthorBioViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'books', BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),  # all DRF endpoints
    path('authors-template/', author_list_view, name='authors_list'),  #template view
    path('contact/', contact_view, name='contact'),
    path('login/', LoginAPIView.as_view(), name='login'), #login view
    path('signup/', SignupAPIView.as_view(), name='signup'), #signup view
]