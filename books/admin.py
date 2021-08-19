from django.contrib import admin
from .models import Book, ReviewComment, BookReview


# Register your models here.
class BooksAdmin(admin.ModelAdmin):
    filter_horizontal = ('authors',)

    def get_queryset(self, request):
        queryset = super(BooksAdmin, self).get_queryset(request).prefetch_related('authors')
        return queryset


class BookReviewAdmin(admin.ModelAdmin):
    fields = ('body', 'book')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class ReviewCommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BooksAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(ReviewComment, ReviewCommentAdmin)

