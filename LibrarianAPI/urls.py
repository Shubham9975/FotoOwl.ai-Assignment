from django.urls import path
from .views import LibraryUserListAPIView, CreateBookAPIView, BookListAPIView, BorrowRequestListView, \
    PendingBorrowRequestListView, BorrowRequestUpdateView, CreateLibraryUserAPIView
from UsersAPI.views import UserRequestHistoryView


urlpatterns = [
    path('', LibraryUserListAPIView.as_view(), name='library-user-list'),
    path('createBook', CreateBookAPIView.as_view(), name='create-book'),
    path('createUser', CreateLibraryUserAPIView.as_view(), name='create-library-user'),
    path('books', BookListAPIView.as_view(), name='book-list'),
    path('borrowRequests/', BorrowRequestListView.as_view(), name='borrow_request_list'),
    path('<int:user_id>/requestHistory/', UserRequestHistoryView.as_view(), name='user_request_history'),
    path('pendingBorrowRequests/', PendingBorrowRequestListView.as_view(), name='pending_borrow_request_list'),
    path('<int:request_id>/borrowRequest/', BorrowRequestUpdateView.as_view(), name='borrow_request_update'),
]
