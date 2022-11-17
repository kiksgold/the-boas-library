from django.contrib import admin
from .models import Book, Review, BookInstance
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'slug', 'uploaded_on')
    search_fields = ['title', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'author', 'uploaded_on')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'book', 'uploaded_on', 'approved')
    list_filter = ('approved', 'uploaded_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'id', 'status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
