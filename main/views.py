from typing import Any

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Book, Category, Author, Borrowing
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import LoginForm
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, TemplateView, DeleteView
)
from django.urls import reverse_lazy


# def home (request):
#     books = Book.objects.all()
#     new_books = Book.objects.order_by('-publication_date')[:3]
#     categories = Category.objects.all()

#     books_copies_no = new_books.annotate(
#         num_copies=Count('bookcopy')
#     )
#     return render(request, 'index.html', {'books': books, 'new_books': books_copies_no, 'categories': categories})

# TemplateView ###############

class AboutPageView (TemplateView):
    template_name = 'about.html'



class HomePageView (TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()
        context['new_books'] = Book.objects.order_by('-publication_date')[:3]
        context['categories'] = Category.objects.all()
        context['books_copies_no'] = context['new_books'].annotate(
            num_copies=Count('bookcopy')
        )
        return context
    
def one_book (request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'one_book.html', {'book': book})

def one_category (request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'one_category.html', {'category': category})

def one_author (request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'one_author.html', {'author': author})
from django.shortcuts import render
from .models import Book, Author, Category

def all_books(request):
    # GET FILTER VALUES
    author_id = request.GET.get("author")
    category_id = request.GET.get("category")

    books = Book.objects.all()

    if author_id and author_id != "":
        books = books.filter(author_id=author_id)

    if category_id and category_id != "":
        books = books.filter(category_id=category_id)

    params = request.GET.copy()
    if "page" in params:
        params.pop("page")

    # PAGINATION (after filtering)
    paginator = Paginator(books, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    # SEND OPTIONS TO TEMPLATE
    authors = Author.objects.all()
    categories = Category.objects.all()

    return render(request, "all_books.html", {
        "page_obj": page_obj,
        "authors": authors,
        "categories": categories,
        "selected_author": author_id,
        "selected_category": category_id,
        "params": params.urlencode(),
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                elif user.groups.filter(name='Members').exists():
                    return redirect('member_profile')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def member_profile(request):
    # how many books have been borrowed
    borrowed_books = Borrowing.objects.filter(member__user=request.user, is_returned=False).count()

    # how many fines have been paid
    fines_paid = Borrowing.objects.filter(member__user=request.user, penalty__gt=0).aggregate(Count('penalty')) ['penalty__count'] or 0
    
    return render(request, 'member_profile.html', {'borrowed_books': borrowed_books, 'fines_paid': fines_paid})


####### ListView ############

class BookListView(ListView):
    model = Book
    template_name = "dashboard/book_list.html"
    context_object_name = "books"
    ordering = ['title']

class BookDetailView(DetailView):
    model = Book
    template_name = "dashboard/book_detail.html"



class BookCreateView(CreateView):
    model = Book
    fields = ["title", "description", "author",
               "category", "publication_date",
                 "isbn", "cover_image"]
    template_name = "dashboard/book_form.html"
    success_url = reverse_lazy("books")

class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "description", "author", "category", 
              "publication_date", "isbn", "cover_image"]
    template_name = "dashboard/book_form.html"
    success_url = reverse_lazy("books")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "dashboard/book_confirm_delete.html"
    success_url = reverse_lazy("books")


class ListViewGeneric (ListView):
    model = None
    title = "Library"
    template_name = "dash/list_view.html"
    context_object_name = "objects"
    columns = None
    add_url = None
    update_url = None
    delete_url = None
    detail_url = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['columns'] = self.columns
        context['add_url'] = self.add_url
        context['update_url'] = self.update_url 
        context['delete_url'] = self.delete_url
        context['detail_url'] = self.detail_url
        return context

    def get_queryset(self):
        return self.model.objects.all()

class BooksListView (ListViewGeneric):
    model = Book
    title = "Books"
    columns = ["title", "author", "category"]
    add_url = reverse_lazy("add_book")
    update_url = ("update_book")
    delete_url = ("delete_book")
    detail_url = ("book_detail")

class CategoryListView(ListViewGeneric):
    model = Category
    title = "Categories"
    columns = ["name"]
    add_url = reverse_lazy("add_category")
    update_url = ("update_category")
    delete_url = ("delete_category")
    detail_url = ("category_detail")    

class AuthorListView(ListViewGeneric):
    model = Author
    title = "Authors"
    columns = ["name", "about"]
    add_url = reverse_lazy("add_author")
    update_url = ("update_author") 
    delete_url = ("delete_author")
    detail_url = ("author_detail")

class AddBookView(CreateView):
    model = Book
    fields = ["title", "description", "author",
               "category", "publication_date",
                 "isbn", "cover_image"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("books")

class AddCategoryView(CreateView):
    model = Category
    fields = ["name", "icon"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("categories")

class AddAuthorView(CreateView):
    model = Author
    fields = ["name", "about"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("authors")

class UpdateBookView(UpdateView):
    model = Book
    fields = ["title", "description", "author", "category", 
              "publication_date", "isbn", "cover_image"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("books")

class UpdateCategoryView(UpdateView):
    model = Category
    fields = ["name", "icon"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("categories")

class UpdateAuthorView(UpdateView):
    model = Author
    fields = ["name", "about"]
    template_name = "dash/base_form.html"
    success_url = reverse_lazy("authors")

class DeleteBookView(DeleteView):
    model = Book
    template_name = "dash/confirm_delete.html"
    success_url = reverse_lazy("books") 

class DeleteCategoryView(DeleteView):
    model = Category
    template_name = "dash/confirm_delete.html"
    success_url = reverse_lazy("categories")

class DeleteAuthorView(DeleteView):
    model = Author
    template_name = "dash/confirm_delete.html"
    success_url = reverse_lazy("authors")

class DetailViewGeneric (DetailView):
    model = None
    template_name = "dash/base_detail.html"
    context_object_name = "object"
    list_url = None
    update_url = None
    delete_url = None
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        context['list_url'] = self.list_url
        context['update_url'] = self.update_url
        context['delete_url'] = self.delete_url
        context['fields'] = [field for field in self.object._meta.get_fields() if field.concrete]
        fields_info = []
        for field in self.object._meta.get_fields():
            if not getattr(field, 'concrete', False):
                continue
            value = getattr(self.object, field.name)
            fields_info.append({
                'label': field.verbose_name,
                'value': value,
                'is_image': field.__class__.__name__ == "ImageField",
                'is_many_to_many': field.__class__.__name__ == "ManyToManyField",
            })
        context['fields_info'] = fields_info

        return context

class BookDetailView(DetailViewGeneric):
    model = Book
    template_name = "dash/base_detail.html"
    context_object_name = "book"
    list_url = "books"
    update_url = "update_book"
    delete_url = "delete_book"



class CategoryDetailView(DetailViewGeneric):
    model = Category
    template_name = "dash/base_detail.html"
    context_object_name = "category"
    list_url = "categories"
    update_url = "update_category"
    delete_url = "delete_category"

class AuthorDetailView(DetailViewGeneric):
    model = Author
    template_name = "dash/base_detail.html"
    context_object_name = "author"
    list_url = "authors"
    update_url = "update_author"
    delete_url = "delete_author"
