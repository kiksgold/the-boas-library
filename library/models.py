from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid


class Book(models.Model):
    # Model representing a book
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="library_books")
    cover_image = CloudinaryField('image', default='placeholder')
    summary = models.TextField(help_text='Enter a brief description of the book', blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='librarybook_like', blank=True)

    class Meta:
        ordering = ["-uploaded_on"]

    def __str__(self):
        # String for representing the Model Object
        return self.title

    def number_of_likes(self):
        # Returns the number of likes on a book
        return self.likes.count()

    def get_absolute_url(self):
        # Returns the URL to access a detail record for this book.
        return reverse('book-detail', args=[str(self.id)])


class Review(models.Model):
    # Model Representing the reviews on a book
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["uploaded_on"]

    def __str__(self):
        # String for representing the Model Object
        return f"Reviews {self.body} by {self.name}"


class BookInstance(models.Model):
    # Model representing a specific book that can be borrowed from the library.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        # String for representing the Model object.
        return f'{self.id} ({self.book.title})'
