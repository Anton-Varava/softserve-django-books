from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, BookReview, ReviewComment
from .forms import BookForm, ReviewCommentForm, BookReviewForm
from .utils import IsAuthorOrStaffMixin, IsOwnerOrStaff


# <-------   Views for Book model ------>
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
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
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('book-search')
        return context


class BookDetailView(DetailView):
    context_object_name = 'book'
    queryset = Book.objects.prefetch_related('authors')

    def get_context_data(self, **kwargs):
        """ Add book reviews data to context with related comments. """
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['reviews'] = BookReview.objects.filter(book=self.kwargs['pk']).select_related('user')\
            .order_by('date_added').prefetch_related('comments', 'comments__user')
        return context


class BookUpdateView(PermissionRequiredMixin, IsAuthorOrStaffMixin, UpdateView):
    permission_required = 'books.change_book'
    model = Book
    form_class = BookForm
    context_object_name = 'book'

    def get_success_url(self):
        """ Return to the updated book details. """
        pk = self.kwargs['pk']
        return reverse('books:detail-book', kwargs={'pk': pk})


class BookCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_book'
    model = Book
    form_class = BookForm

    def get_success_url(self):
        """ Return to the created book details. """
        return reverse('books:detail-book', args=(self.object.id, ))


class BookDeleteView(PermissionRequiredMixin, IsAuthorOrStaffMixin, DeleteView):
    permission_required = 'books.delete_book'
    model = Book

    def get_success_url(self):
        return reverse('books:list-book')

    def get_context_data(self, **kwargs):
        """ Add book data to context for using it in a template. """
        context = super(BookDeleteView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['pk'])
        return context


# <-------   Views for BookReview model ------>
class BookReviewCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'books.add_bookreview'
    model = BookReview
    form_class = BookReviewForm

    def post(self, request, *args, **kwargs):
        """ Add current user and book instance to form data before saving. """
        form = BookReviewForm(request.POST)
        user = self.request.user
        book = Book.objects.get(id=self.kwargs['book_id'])

        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.book = book
            form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """ Add book data to context for using it in a template. """
        context = super(BookReviewCreateView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])

        return context

    def get_success_url(self):
        """ Return to the book details. """
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class BookReviewDeleteView(PermissionRequiredMixin, IsOwnerOrStaff, DeleteView):
    permission_required = 'books.delete_bookreview'
    model = BookReview

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(BookReviewDeleteView, self).get_context_data(**kwargs)
        context['review_id'] = self.kwargs['pk']
        context['book_id'] = self.kwargs['book_id']
        return context


class BookReviewUpdateView(PermissionRequiredMixin, IsOwnerOrStaff, UpdateView):
    permission_required = 'books.change_bookreview'
    model = BookReview
    form_class = BookReviewForm

    def get_context_data(self, **kwargs):
        context = super(BookReviewUpdateView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])
        context['review_id'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


# <-------   Views for ReviewComment model ------>
class CommentReviewCreateView(LoginRequiredMixin, CreateView):
    model = ReviewComment
    form_class = ReviewCommentForm

    def get_initial(self):
        """ Pre-populating form if it's a reply. """
        initial = super(CommentReviewCreateView, self).get_initial()
        if 'reply_id' in self.kwargs:
            parent_comment = get_object_or_404(ReviewComment, id=self.kwargs['reply_id'])
            initial['body'] = f'<q>{parent_comment.body}</q><br/>'
        return initial

    def post(self, request, *args, **kwargs):
        """ Add current user and review instance to form data before saving. """
        form = ReviewCommentForm(request.POST)
        review = BookReview.objects.get(id=self.kwargs['review_id'])
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.review = review
            form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CommentReviewCreateView, self).get_context_data(**kwargs)
        context['book_id'] = self.kwargs['book_id']

        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class CommentUpdateView(LoginRequiredMixin, IsOwnerOrStaff, UpdateView):
    model = ReviewComment
    form_class = ReviewCommentForm

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context['comment_id'] = self.kwargs['pk']
        context['book_id'] = self.kwargs['book_id']
        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class CommentDeleteView(LoginRequiredMixin, IsOwnerOrStaff, DeleteView):
    model = ReviewComment

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context['comment'] = ReviewComment.objects.get(id=self.kwargs['pk'])
        context['book_id'] = self.kwargs['book_id']
        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})
