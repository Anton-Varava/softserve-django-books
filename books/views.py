from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, BookReview, ReviewComment
from .forms import BookUpdateForm, BookCreateForm, BookReviewCreateForm, ReviewCommentCreateForm, \
    ReviewCommentUpdateForm, BookReviewUpdateForm


# <-------   Views for Book model ------>
class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('book-search')
        ordering = '-popularity_rank'
        if query:
            queryset = Book.objects.filter(
                Q(title__icontains=query) | Q(isbn13=query)).prefetch_related('authors').order_by(ordering)
        else:
            queryset = Book.objects.prefetch_related('authors').order_by(ordering)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_search'] = self.request.GET.get('book-search')
        return context


class BookDetailView(DetailView):
    context_object_name = 'book'
    queryset = Book.objects.prefetch_related('authors')

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['reviews'] = BookReview.objects.filter(book=self.kwargs['pk']).select_related('user').prefetch_related('comments')
        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookUpdateForm
    success_message = 'Book updated successfully.'
    template_name = 'books/book_form.html'
    context_object_name = 'book'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('books:detail-book', kwargs={'pk': pk})


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookCreateForm

    def get_success_url(self):
        return reverse('books:detail-book', args=(self.object.id, ))


# <-------   Views for BookReview model ------>
class BookReviewListView(ListView):
    model = BookReview
    context_object_name = 'reviews'


class BookReviewCreateView(LoginRequiredMixin, CreateView):
    model = BookReview
    form_class = BookReviewCreateForm

    def post(self, request, *args, **kwargs):
        form = BookReviewCreateForm(request.POST)
        user = self.request.user
        book = Book.objects.get(id=self.kwargs['book_id'])

        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.book = book
            form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(BookReviewCreateView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])

        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class BookReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = BookReview

    def get_object(self, queryset=None):
        obj = super(BookReviewDeleteView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(BookReviewDeleteView, self).get_context_data(**kwargs)
        context['review_id'] = self.kwargs['pk']
        context['book_id'] = self.kwargs['book_id']
        return context


class BookReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = BookReview
    form_class = BookReviewUpdateForm

    def get_context_data(self, **kwargs):
        context = super(BookReviewUpdateView, self).get_context_data(**kwargs)
        context['book'] = Book.objects.get(id=self.kwargs['book_id'])
        context['review_id'] = self.kwargs['pk']
        return context

    def get_object(self, queryset=None):
        obj = super(BookReviewUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


# <-------   Views for ReviewComment model ------>
class CommentReviewCreateView(LoginRequiredMixin, CreateView):
    model = ReviewComment
    form_class = ReviewCommentCreateForm

    def get_initial(self):
        initial = super(CommentReviewCreateView, self).get_initial()
        if self.kwargs['reply_id']:
            parent_comment = get_object_or_404(ReviewComment, id=self.kwargs['reply_id'])
            initial['body'] = f'<q>{parent_comment.body}</q><br/>'
        return initial

    def post(self, request, *args, **kwargs):
        form = ReviewCommentCreateForm(request.POST)
        user = self.request.user
        review = BookReview.objects.get(id=self.kwargs['review_id'])
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.review = review
            form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CommentReviewCreateView, self).get_context_data(**kwargs)
        context['book_id'] = self.kwargs['book_id']
        if self.kwargs['reply_id']:
            context['reply_body'] = ReviewComment.objects.get(id=self.kwargs['reply_id'])
        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = ReviewComment
    form_class = ReviewCommentUpdateForm

    def get_object(self, queryset=None):
        obj = super(CommentUpdateView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context['comment_id'] = self.kwargs['pk']
        context['book_id'] = self.kwargs['book_id']
        return context

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = ReviewComment

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context['comment'] = ReviewComment.objects.get(id=self.kwargs['pk'])
        context['book_id'] = self.kwargs['book_id']
        return context

    def get_object(self, queryset=None):
        obj = super(CommentDeleteView, self).get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        pk = self.kwargs['book_id']
        return reverse('books:detail-book', kwargs={'pk': pk})
        










