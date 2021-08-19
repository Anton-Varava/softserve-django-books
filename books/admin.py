from django.contrib import admin
from .models import Book, ReviewComment, BookReview


# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(BooksAdmin, self).get_queryset(request).prefetch_related('authors')
        return queryset


class BookReviewAdmin(admin.ModelAdmin):
    pass


class ReviewCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BooksAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(ReviewComment, ReviewCommentAdmin)

