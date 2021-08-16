from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.title}" {self.author}'


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

