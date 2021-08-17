from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, blank=True)
    # image = models.ImageField(default='default_author.jpg', upload_to='authors_pics')
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
