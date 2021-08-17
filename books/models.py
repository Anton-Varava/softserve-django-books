from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from authors.models import Author


# Create your models here.
class Book(models.Model):
    isbn13 = models.CharField(max_length=13, blank=True, unique=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2000, null=True)
    authors = models.ManyToManyField(Author)
    popularity_rank = models.PositiveSmallIntegerField(default=1,
                                                       validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'"{self.title}" ({self.isbn13})'


class BookReview(models.Model):
    text = models.TextField(max_length=1000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class ReviewComment(models.Model):
    text = models.TextField(max_length=1000)
    review = models.ForeignKey(BookReview, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

