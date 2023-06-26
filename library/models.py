from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class Genre(models.Model):
    name = models.CharField(max_length=32)
    objects = models.Manager() #по умолчанию используемый (models.Manager())
    # books (с связи many-to-many)

    def __str__(self):
        return self.name

    def url_detail(self):
        return reverse('lib:genre-list') + f'#g-{self.id}'

    class Meta:
        ordering = ['name']


class Author(models.Model):
    first = models.CharField(max_length=32)
    last = models.CharField(max_length=32, null=True, blank=True)
    born = models.DateField(null=True, blank=True)
    portrait = models.URLField(null=True, blank=True)
    objects = models.Manager() #по умолчанию используемый (models.Manager())
    # books

    def __str__(self):
        return self.first + ' ' + self.last

    def url_detail(self):
        return reverse('lib:author-detail', kwargs={'pk': self.id})

    def genres(self):
        return Genre.objects.filter(books__author__exact=self).distinct()
        #distinct() - сузить выборку, убрав повторы (в нашем случае повторы жанров на страничке автора)

    def comments(self):
        return Comment.objects.filter(book__author__exact=self).select_related('book').all()


class Book(models.Model):
    title = models.CharField(max_length=128)
    cover = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    # связь one-to-many
    author = models.ForeignKey(Author, related_name='books',
            on_delete=models.SET_NULL, null=True, blank=True)

    # связь many-to-many (связь с жанрами)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True) #blank=True - позволяет создавать книгу (записывать её в базу), где я могу не указывать ни одного жанра
    # в противном случае, если не будет blank=True, мы не сможем записать книгу, у которой не будет ни одного жанра
    objects = models.Manager() #по умолчанию используемый (models.Manager())

    # comments
    # instances (экземпляры)

    def __str__(self):
        return self.title

    def url_detail(self):
        return reverse('lib:book-detail', kwargs={'pk': self.id})


class Comment(models.Model):
    user = models.CharField(max_length=32)
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created'] #по убыванию


STATUSES = [
    ('a', 'Available'), #книга доступна
    ('o', 'On loan'), #книга у кого-то на руках
]


class Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, related_name='instances', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUSES, default='a') #default - по умолчанию книга доступна
    due_back = models.DateField(null=True, blank=True)

    def url_detail(self):
        return reverse('lib:instance-detail', kwargs={'pk': self.id})
