from django.contrib import admin

from .models import *


class BookInLine(admin.TabularInline):
    model = Book
    max_num = 3


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInLine]
    list_display = ['last', 'first', 'born']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']


@admin.register(Comment)
class BookAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'book', 'created']


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back', 'id']

