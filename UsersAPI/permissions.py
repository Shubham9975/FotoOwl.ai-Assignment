from rest_framework import permissions
from LibrarianAPI.models import LibraryUser


class IsLibraryUser(permissions.BasePermission):
    """
    Custom permission to grant access only to LibraryUser.
    """

    def has_permission(self, request, view):
        # Check if the request has a valid token and user is a LibraryUser
        user = request.user
        if user.is_authenticated:
            return isinstance(user, LibraryUser)
        return False
