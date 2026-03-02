from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination

class BasePagination:
    page_size = 10                      #By default, 10 books go in one box
    page_size_query_param = 'page_size' #Customer can ask for a different number of books per box
    max_page_size = 50                  #But we will never put more than 50 books in a box, even if they ask

class BooksPagination(PageNumberPagination, BasePagination):
    page_size = 5  # override default 10 to 5

class AuthorsPagination(PageNumberPagination, BasePagination):
    max_page_size = 20 #override default 50 to 20


class GenrePagination(PageNumberPagination, BasePagination):
    page_size_query_param = 'limit'  # client uses ?limit=5 instead of ?page_size=5


class BooksCursorPagination(CursorPagination, BasePagination):
    page_size = 5
    ordering = 'created_at'  # newest books first