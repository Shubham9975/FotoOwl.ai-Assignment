from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LibraryUser
from .models import BorrowRequest, BorrowRequestHistory, Books


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_librarian', 'is_staff', 'is_active')
    list_filter = ('is_librarian', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_librarian',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_librarian',)}),
    )


@admin.register(LibraryUser)
class LibraryUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password')


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    model = Books
    list_display = ('book_id', 'title', 'author', 'description')
    search_fields = ('book_id', 'title', 'author')
    ordering = ('title',)


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    model = BorrowRequest
    list_display = ('user', 'book', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__name', 'book__title', 'status')
    ordering = ('start_date',)


@admin.register(BorrowRequestHistory)
class BorrowRequestHistoryAdmin(admin.ModelAdmin):
    model = BorrowRequestHistory
    list_display = ('request', 'user', 'book', 'action', 'start_date', 'end_date')
    list_filter = ('action', 'start_date', 'end_date')
    search_fields = ('user__name', 'book__title', 'action')
    ordering = ('start_date',)
