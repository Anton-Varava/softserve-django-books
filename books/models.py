from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# from django.contrib.auth.models import User
from users.models import User
from authors.models import Author


# Create your models here.
class Book(models.Model):
    isbn13 = models.CharField(max_length=13, blank=True, unique=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2000, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    popularity_rank = models.PositiveSmallIntegerField(default=1,
                                                       validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.title} by {", ".join(author.__str__() for author in self.authors.all())}'


class BookReview(models.Model):
    body = models.TextField(max_length=1000)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class ReviewComment(models.Model):
    body = models.TextField(max_length=1000)
    review = models.ForeignKey(BookReview, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

