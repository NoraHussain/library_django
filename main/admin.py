from django.contrib import admin

from main.models import Author, Book, BookCopy, Category, Member, Borrowing

admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Member)
admin.site.register(Borrowing)
