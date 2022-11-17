from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Book


class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.all().order_by('-uploaded_on')
    template_name = 'index.html'
    paginate_by = 6


class BookDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Book.objects.filter()
        book = get_object_or_404(queryset, slug=slug)
        reviews = book.reviews.filter(approved=True).order_by('uploaded_on')
        liked = False
        if book.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "reviews": reviews,
                "liked": liked,

            }
        )
