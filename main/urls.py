from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('one_book/<int:book_id>/', views.one_book, name='one_book'),
    path('one_category/<int:category_id>/', views.one_category, name='one_category'),
    path('one_author/<int:author_id>/', views.one_author, name='one_author'),
    path('all_books/', views.all_books, name='all_books'),
    path('member_profile/', views.member_profile, name='member_profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('dashboard/books/', views.BookListView.as_view(), name='books'),
    path('dashboard/books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('dashboard/books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('dashboard/books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('dashboard/books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),

    path('dash/books', views.BooksListView.as_view(), name='books'),
    path('dash/categories/', views.CategoryListView.as_view(), name='categories'),
    path('dash/authors/', views.AuthorListView.as_view(), name='authors'),

    path('dash/books/add/', views.AddBookView.as_view(), name='add_book'),
    path('dash/categories/add/', views.AddCategoryView.as_view(), name='add_category'),
    path('dash/authors/add/', views.AddAuthorView.as_view(), name='add_author'),

    path('dash/books/<int:pk>/edit/', views.UpdateBookView.as_view(), name='update_book'),
    path('dash/categories/<int:pk>/edit/', views.UpdateCategoryView.as_view(), name='update_category'),
    path('dash/authors/<int:pk>/edit/', views.UpdateAuthorView.as_view(), name='update_author'),

    path('dash/books/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete_book'),
    path('dash/categories/<int:pk>/delete/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('dash/authors/<int:pk>/delete/', views.DeleteAuthorView.as_view(), name='delete_author'),

    path('dash/books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('dash/categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('dash/authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

]