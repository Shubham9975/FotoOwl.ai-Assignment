from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'is_librarian') and request.user.is_librarian
