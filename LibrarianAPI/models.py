from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.


class CustomUser(AbstractUser):
    is_librarian = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Librarian"


class LibraryUser(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name}"

    def set_password(self, raw_password):
        """Hashes the password using Django's hashing function."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the given password matches the hashed one."""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name}"


class Books(models.Model):
    book_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "Books"


class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ]

    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.name} request"


class BorrowRequestHistory(models.Model):
    request = models.ForeignKey(BorrowRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
