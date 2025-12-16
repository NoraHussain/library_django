from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()

    def __str__(self):
        return str(self.name)

class Category (models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField()

    def __str__(self):
        return self.name

class Book (models.Model):
    title = models.CharField()
    description = models.CharField()
    cover_image = models.ImageField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ManyToManyField(Category, related_name='books')
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True) 

class Borrowing(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)