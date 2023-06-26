from django.urls import path

from . import views

app_name = 'lib'

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.IndexTemplateView.as_view(), name='home'),

    # path('book/list/', views.book_list, name='book-list'),
    path('book/list/', views.BookListView.as_view(), name='book-list'),

    path('author/list/', views.author_list, name='author-list'),
    path('genre/list/', views.genre_list, name='genre-list'),
    # path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # path('author/<int:pk>/', views.author_detail, name='author-detail'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),

    path('comment/<int:pk>/add/form/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/add/model/', views.add_comment_modelform, name='add-comment-model'),

    path('instance/<uuid:pk>/', views.instance_detail, name='instance-detail'),
    path('lend/instance/<uuid:pk>/', views.lend_instance, name='lend-instance'),

    path('api/book/list/', views.BookListAPIView.as_view()),
    path('api/book/<int:pk>/', views.BookDetailAPIView.as_view()),

]

