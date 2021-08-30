from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.db.models import Q
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from authors.models import Author

from .models import Book, BookReview, ReviewComment
from .forms import BookForm, ReviewCommentForm, BookReviewForm
from .utils import IsOwnerOrStaff


# <-------   Views for Book model ------>
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        """ Return a queryset of all or filtered objects. """
        query = self.request.GET.get('book-search', None)
        ordering = '-popularity_rank'
        if query:
            queryset = Book.objects.filter(
                Q(title__icontains=query) | Q(isbn13=query)).prefetch_related('authors').order_by(ordering)
        else:
            queryset = Book.objects.prefetch_related('authors').order_by(ordering)
        return queryset

    def get_context_data(self, *args, **kwargs):
        """ Add search_query to context for using in template. """
        context = super().get_context_data(*args, **kwargs)
        context['search_query'] = self.request.GET.get('book-search')
        return context


class BookDetailView(DetailView):
    context_object_name = 'book'

    def get_object(self, queryset=None):
        try:
            book = Book.objects.prefetch_related('authors').get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted')
        return book

    def get_context_data(self, **kwargs):
        """ Add book reviews data to a context with a related review comments. """
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['reviews'] = BookReview.objects.filter(book=self.kwargs.get('pk')).select_related('user')\
            .order_by('date_added').prefetch_related('comments', 'comments__user')
        if self.request.user.is_authenticated:
            author = Author.objects.filter(user=self.request.user).first()
            context['is_author'] = (True if author and author in self.object.authors.all() else False)
        return context


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'books.change_book'
    form_class = BookForm
    context_object_name = 'book'

    def get_object(self, queryset=None):
        try:
            book = Book.objects.prefetch_related('authors').get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted')

        # Check that user is a staff or is a book author.
        author = Author.objects.filter(user=self.request.user).first()
        if self.request.user.is_staff or author and author in book.authors.all():
            return book
        raise PermissionDenied('You don\'t have permission to edit this book ')


class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_book'
    model = Book
    form_class = BookForm

    def form_valid(self, form):
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            raise PermissionDenied('You must be an author to create books.')
        form.save()  # We need to save before adding authors
        form.instance.authors.add(author)
        return super(BookCreateView, self).form_valid(form)


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'books.delete_book'

    def get_success_url(self):
        return reverse('books:list-book')

    def get_context_data(self, **kwargs):
        """ Add book data to context for using it in a template. """
        context = super(BookDeleteView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs.get('pk'))
        return context

    def get_object(self, queryset=None):
        try:
            book = Book.objects.prefetch_related('authors').get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted')

        """ Check that user is a staff or is book author. """
        author = Author.objects.filter(user=self.request.user).first()
        if self.request.user.is_staff or author and author in book.authors.all():
            return book
        raise PermissionDenied('You don\'t have permission to delete this book ')


# <-------   Views for BookReview model ------>
class BookReviewCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_bookreview'
    model = BookReview
    form_class = BookReviewForm

    def form_valid(self, form):
        """ Add current user and book instance to form data before saving. """
        try:
            form.instance.book = Book.objects.get(id=self.kwargs.get('book_id'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted.')
        form.instance.user = self.request.user
        return super(BookReviewCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """ Add book data to context for using it in a template. """
        context = super(BookReviewCreateView, self).get_context_data(**kwargs)
        try:
            context['book'] = Book.objects.get(id=self.kwargs.get('book_id'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted.')
        return context


class BookReviewDeleteView(PermissionRequiredMixin, IsOwnerOrStaff, DeleteView):
    permission_required = 'books.delete_bookreview'
    model = BookReview

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(BookReviewDeleteView, self).get_context_data(**kwargs)
        context['review_id'] = self.kwargs.get('pk')
        context['book_id'] = self.kwargs.get('book_id')
        return context


class BookReviewUpdateView(PermissionRequiredMixin, IsOwnerOrStaff, UpdateView):
    permission_required = 'books.change_bookreview'
    model = BookReview
    form_class = BookReviewForm

    def get_context_data(self, **kwargs):
        context = super(BookReviewUpdateView, self).get_context_data(**kwargs)
        try:
            context['book'] = Book.objects.get(id=self.kwargs.get('book_id'))
        except ObjectDoesNotExist:
            raise Http404('The book does not exist or has been deleted')
        context['review_id'] = self.kwargs.get('pk')
        return context


# <-------   Views for ReviewComment model ------>
class CommentReviewCreateView(LoginRequiredMixin, CreateView):
    model = ReviewComment
    form_class = ReviewCommentForm

    def get_initial(self):
        """ Pre-populating form if it's a reply. """
        initial = super(CommentReviewCreateView, self).get_initial()
        if 'reply_id' in self.kwargs:
            parent_comment = get_object_or_404(ReviewComment, id=self.kwargs.get('reply_id'))
            initial['body'] = f'<q>{parent_comment.body}</q><br/>'
        return initial

    def form_valid(self, form):
        """ Add current user and review instance to form data before saving. """
        try:
            form.instance.review = BookReview.objects.get(id=self.kwargs.get('review_id'))
        except ObjectDoesNotExist:
            raise Http404('The review does not exist or has been deleted.')
        form.instance.user = self.request.user
        return super(CommentReviewCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CommentReviewCreateView, self).get_context_data(**kwargs)
        context['book_id'] = self.kwargs.get('book_id')
        return context


class CommentUpdateView(LoginRequiredMixin, IsOwnerOrStaff, UpdateView):
    model = ReviewComment
    form_class = ReviewCommentForm

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context['comment_id'] = self.kwargs.get('pk')
        context['book_id'] = self.kwargs.get('book_id')
        return context


class CommentDeleteView(LoginRequiredMixin, IsOwnerOrStaff, DeleteView):
    model = ReviewComment

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        try:
            context['comment'] = ReviewComment.objects.get(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise Http404('The comment does not exist or has been deleted.')
        context['book_id'] = self.kwargs.get('book_id')
        return context

    def get_success_url(self):
        return self.object.get_absolute_url()
