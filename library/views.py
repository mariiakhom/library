from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework.generics import ListAPIView, RetrieveAPIView

from .forms import CommentForm
from .models import *
from .serializers import *

# def index(request):
#     return render(request,
#                   template_name='Library/index.html',
#                   context={
#                     'n1': Book.objects.count(),
#                     'n2': Author.objects.count(),
#                     'n3': Genre.objects.count(),
#                   })


class IndexTemplateView(TemplateView):
    template_name = 'Library/index.html'
    extra_context = {
                    'n1': Book.objects.count(),
                    'n2': Author.objects.count(),
                    'n3': Genre.objects.count(),
                    }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['n1'] = Book.objects.count()
    #     context['n2'] = Author.objects.count()
    #     context['n3'] = Genre.objects.count()
    #     return context


# def book_list(request):
#     return render(request,
#                   template_name='Library/book_list.html',
#                   context={
#                     'object_list': Book.objects.order_by('title')\
#                         .annotate(number_of_comments=Count('comments'))\
#                         .prefetch_related('genres'),
#                   })


class BookListView(ListView):
    model = Book
    queryset = Book.objects.order_by('title')\
                        .annotate(number_of_comments=Count('comments'))\
                        .prefetch_related('genres')


def author_list(request):
    return render(request,
                  template_name='Library/author_list.html',
                  context={
                    'object_list': Author.objects.order_by('last', 'first')\
                    .annotate(number_of_books=Count('books'), number_of_comments=Count('books__comments')),
                  })


def genre_list(request):
    return render(request,
                  template_name='Library/genre_list.html',
                  context={
                    'object_list': Genre.objects.order_by('name'),
                  })


# def book_detail(request, pk):
#     return render(request,
#                   template_name='Library/book_detail.html',
#                   context={
#                     'object': Book.objects.select_related('author').get(id__exact=pk),
#                   })


class BookDetailView(DetailView):
    model = Book
    extra_context = {
        'cf': CommentForm(),
    }

    # def get_object(self, queryset=None):
    #     obj = super(BookDetailView, self).get_object(queryset=queryset)
    #     obj = Book.objects.select_related('author').get(id__exact=obj.id)
    #     return obj


# def author_detail(request, pk):
#     return render(request,
#                   template_name='Library/author_detail.html',
#                   context={
#                     'object': Author.objects.get(id__exact=pk),
#                     'comments': Comment.objects.filter(book__author__id__exact=pk).select_related('book').all()
#                   })


class AuthorDetailView(DetailView):
    model = Author


    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        print([context])
        context['comments'] = Comment.objects.filter(book__author__id__exact=self.object.id).select_related('book').all()
        context['num_comments'] = len(context['comments'])
        print([context])
        return context


def add_comment(request, pk): #pk - индекс книги
    book = Book.objects.get(pk=pk)
    print(request.POST)
    user = request.POST.get('user')
    text = request.POST.get('text')
    # будем создавать комментарий, если user и text не пустые
    if user and text:
        Comment.objects.create(
            text=text,
            user=user,
            book=book, #тоже самое что и book_id=pk
        )
    return HttpResponseRedirect(book.url_detail())


def add_comment_modelform(request, pk):
    book = Book.objects.get(pk=pk)
    f = CommentForm(request.POST)
    if f.is_valid():
        new_comment = f.save(commit=False)
        print('new_comment', new_comment)
        new_comment.book = book
        new_comment.save()
    else:
        print(f.errors)

    return HttpResponseRedirect(book.url_detail())


def instance_detail(request, pk):
    return render(request,
                  template_name='Library/instance_detail.html',
                  context={
                      'object': Instance.objects.get(id__exact=pk),
                  })

def lend_instance(request, pk):
    due_back = request.POST.get('due_back')
    instance = Instance.objects.get(pk=pk)
    if due_back:
        print(due_back)
        instance.due_back = due_back
        instance.status = 'o'
        instance.save()
    return HttpResponseRedirect(instance.book.url_detail())


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer1
    queryset = Book.objects.order_by('title')


class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializer2
    queryset = Book.objects.all()
