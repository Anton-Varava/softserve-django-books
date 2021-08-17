from django.contrib import admin
from .models import Author


# Register your models here.
class AuthorsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorsAdmin)

