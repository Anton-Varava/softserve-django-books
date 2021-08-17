from django.contrib import admin
from .models import Book


# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BooksAdmin)

