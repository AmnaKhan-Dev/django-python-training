
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Books, Genre

@receiver(m2m_changed, sender=Books.genres.through)  #this is a signal that is triggered when the genres of a book are changed
def update_genre_book_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        for genre in instance.genres.all():
            count = genre.books.count()
            print(f"Genre '{genre.name}' now has {count} books")