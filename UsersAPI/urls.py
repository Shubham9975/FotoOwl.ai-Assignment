from django.urls import path
from .views import BorrowRequestCreateAPIView, UserRequestHistoryView, \
    DownloadUserRequestHistoryView
from LibrarianAPI.views import BookListAPIView


urlpatterns = [
    path('books', BookListAPIView.as_view(), name='book-list'),
    path('<int:id>/borrowRequest', BorrowRequestCreateAPIView.as_view(), name='create-borrow-request'),
    path('<int:user_id>/requestHistory/', UserRequestHistoryView.as_view(), name='user_request_history'),
    path('<int:user_id>/requestHistory/download/', DownloadUserRequestHistoryView.as_view(), name='download_user_request_history'),
    # path('login/', LibraryUserLoginView.as_view(), name='library_user_login'),
]
