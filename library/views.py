from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Book
from .forms import ReviewForm


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
                "reviewed": False,
                "liked": liked,
                "review_form": ReviewForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Book.objects.filter()
        book = get_object_or_404(queryset, slug=slug)
        reviews = book.reviews.filter(approved=True).order_by("-uploaded_on")
        liked = False
        if book.likes.filter(id=self.request.user.id).exists():
            liked = True

        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review_form.instance.email = request.user.email
            review_form.instance.name = request.user.username
            review = review_form.save(commit=False)
            review.book = book
            review.save()
        else:
            review_form = ReviewForm()

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "reviews": reviews,
                "reviewed": True,
                "review_form": review_form,
                "liked": liked
            },
        )


class BookLike(View):
    
    def post(self, request, slug):
        book = get_object_or_404(Book, slug=slug)
        if book.likes.filter(id=request.user.id).exists():
            book.likes.remove(request.user)
        else:
            book.likes.add(request.user)

        return HttpResponseRedirect(reverse('book_detail', args=[slug]))
