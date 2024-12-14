from rest_framework import serializers
from LibrarianAPI.models import BorrowRequest, BorrowRequestHistory


class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = ['user', 'book', 'start_date', 'end_date', 'status']

    def validate(self, data):
        user = data.get('user')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        overlapping_requests = BorrowRequest.objects.filter(
            user=user,
            status='approved',
            start_date__lt=end_date,
            end_date__gt=start_date
        )

        if overlapping_requests.exists():
            raise serializers.ValidationError("This book is already booked during the requested timeframe.")

        data['status'] = 'pending'
        return data

    def create(self, validated_data):
        borrow_request = BorrowRequest.objects.create(**validated_data)

        BorrowRequestHistory.objects.create(
            request=borrow_request,
            user=borrow_request.user,
            book=borrow_request.book,
            action="Request Created",
            start_date=borrow_request.start_date,
            end_date=borrow_request.end_date
        )

        return borrow_request
