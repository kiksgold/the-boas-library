from django.shortcuts import render
from django.views import generic
from .models import Book


class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.all().order_by('-uploaded_on')
    template_name = 'index.html'
    paginate_by = 6
