from django.db import models
from django.urls import reverse

from users.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('authors:detail-author', kwargs={'pk': self.id})

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
