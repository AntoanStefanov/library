from django.contrib import admin

from .models import Book


# The ModelAdmin class is the representation of a model in the admin interface.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'posted_by')
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields
    # title + author , in case two authors have the same title name for a book.
    prepopulated_fields = {"slug": ("title", "author")}


admin.site.register(Book, BookAdmin)
