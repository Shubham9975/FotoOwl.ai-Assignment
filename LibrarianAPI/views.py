from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LibraryUserSerializer, BookSerializer, BorrowRequestSerializer
from rest_framework import status, permissions
from .models import Books, BorrowRequest, BorrowRequestHistory, LibraryUser
from .permissions import IsLibrarian
from UsersAPI.permissions import IsLibraryUser
from rest_framework.permissions import IsAuthenticated


class CreateLibraryUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Invalid user. Only librarians can create library users."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = LibraryUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryUserListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLibrarian]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Invalid user. Only librarians can view the user list."},
                            status=status.HTTP_403_FORBIDDEN)

        users = LibraryUser.objects.all()
        serializer = LibraryUserSerializer(users, many=True)
        return Response(serializer.data)


class CreateBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response({"error": "Invalid user. Only librarians can create books."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # print("Authenticated User:", request.user)
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BorrowRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Only librarians can view all borrow requests."},
                            status=status.HTTP_403_FORBIDDEN)

        borrow_requests = BorrowRequest.objects.all()
        serializer = BorrowRequestSerializer(borrow_requests, many=True)
        return Response(serializer.data)


class PendingBorrowRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Only librarians can view pending borrow requests."},
                            status=status.HTTP_403_FORBIDDEN)

        pending_requests = BorrowRequest.objects.filter(status='pending')
        serializer = BorrowRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)


class BorrowRequestUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        if not request.user.is_superuser:
            return Response({"error": "Only librarians can update borrow requests."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            borrow_request = BorrowRequest.objects.get(id=request_id)
        except BorrowRequest.DoesNotExist:
            return Response({"error": "Borrow request not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action not in ['approve', 'deny']:
            return Response({"error": "Invalid action. Use 'approve' or 'deny'."}, status=status.HTTP_400_BAD_REQUEST)

        borrow_request.status = 'approved' if action == 'approve' else 'denied'
        action_message = 'Request Approved' if action == 'approve' else 'Request Denied'
        borrow_request.save()

        BorrowRequestHistory.objects.create(
            request=borrow_request,
            user=borrow_request.user,
            book=borrow_request.book,
            action=action_message,
            start_date=borrow_request.start_date,
            end_date=borrow_request.end_date
        )

        return Response({"message": f"{action_message.lower()} successfully."}, status=status.HTTP_200_OK)
