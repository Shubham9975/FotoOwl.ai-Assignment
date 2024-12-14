from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from LibrarianAPI.models import BorrowRequestHistory, Books, BorrowRequest
from UsersAPI.serializers import BorrowRequestSerializer
# from rest_framework.exceptions import ValidationError
import csv
# from rest_framework import permissions
from django.http import HttpResponse
from LibrarianAPI.serializers import BorrowRequestHistorySerializer
from LibrarianAPI.models import LibraryUser
from rest_framework.permissions import IsAuthenticated
from UsersAPI.permissions import IsLibraryUser
from LibrarianAPI.permissions import IsLibrarian
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.urls import reverse
# from django.contrib.auth import login
# from django.shortcuts import redirect


class BorrowRequestCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')

        try:
            user = LibraryUser.objects.get(id=user_id)
        except LibraryUser.DoesNotExist:
            return Response({"error": "Library User not found."}, status=status.HTTP_404_NOT_FOUND)

        book_id = request.data.get('book')
        try:
            book = Books.objects.get(id=book_id)
        except Books.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        overlapping_requests = BorrowRequest.objects.filter(
            user=user,
            status='approved',
            end_date__gte=start_date,
            start_date__lte=end_date
        )

        if overlapping_requests.exists():
            return Response({"error": "The requested dates overlap with an existing borrow request."},
                             status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = user.id

        serializer = BorrowRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRequestHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request, user_id):
        try:
            user = LibraryUser.objects.get(id=user_id)
        except LibraryUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        request_history = BorrowRequestHistory.objects.filter(user=user)
        serializer = BorrowRequestHistorySerializer(request_history, many=True)
        return Response(serializer.data)


class DownloadUserRequestHistoryView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get(self, request, user_id):
        try:
            user = LibraryUser.objects.get(id=user_id)
        except LibraryUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        request_history = BorrowRequestHistory.objects.filter(user=user)

        if not request_history:
            return Response({"message": "No borrow request history found for this user."},
                             status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="user_{user_id}_request_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['Request ID', 'Book ID', 'Book Title', 'Action', 'Start Date', 'End Date'])

        for history in request_history:
            writer.writerow([
                history.request.id,
                history.book.book_id,
                history.book.title,
                history.action,
                history.start_date,
                history.end_date
            ])

        return response

# class LibraryUserLoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Get email and password from the request data
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         if not email or not password:
#             return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # Get user by email
#             user = LibraryUser.objects.get(email=email)
#
#             # Check if the password is correct using the check_password method
#             if not user.check_password(password):
#                 raise AuthenticationFailed("Invalid credentials")
#
#         except LibraryUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = refresh.access_token
#
#         # Store the user in the session (if you're using session-based authentication)
#         request.session['user_id'] = user.id
#
#         # Redirect the user to the borrow request page with the user id
#         borrow_request_url = reverse('create-borrow-request', kwargs={'id': user.id})
#
#         # Return the response with token and redirection URL
#         return Response({
#             'refresh': str(refresh),
#             'access': str(access_token),
#             'redirect_to': borrow_request_url
#         }, status=status.HTTP_200_OK)
