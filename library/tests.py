from django.test import TestCase

from .models import Author, Book, Genre

class AuthorBookGenreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first='John', last='Smith')
        for i in range(5):
            Book.objects.create(title=f'Book-{i}', author=Author.objects.get(id__exact=1))
        b1: Book = Book.objects.get(pk=1)
        g1 = Genre(name='genre-1')
        g1.save()
        b1.genres.add(g1)


    def test_1(self):
        number_of_authors = Author.objects.count()
        self.assertEqual(number_of_authors, 1)
        number_of_books = Book.objects.count()
        self.assertEqual(number_of_books, 5)


    def test_2(self):
        a = Author.objects.get(id__exact=1)
        self.assertTrue(a.books.exists())


    def test_3(self):
        a = Author.objects.get(id__exact=1)
        self.assertEqual(str(a), 'John Smith')
        self.assertNotEqual(str(a), 'Smith John')
        g = Genre.objects.get(id__exact=1)
        self.assertEqual(str(g), 'genre-1')
