from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('biblio', 'Bibliothécaire'),
    ('lecteur', 'Lecteur'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='lecteur')
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    fullname = models.CharField(max_length=200)

    def __str__(self):
        return self.fullname
class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    file = models.FileField(upload_to='books/', null=True, blank=True)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.title





class Reservation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reservation {self.book.title} by {self.user.username}"

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    returned_at = models.DateTimeField(null=True, blank=True)
    sanction = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    def is_overdue(self):
        return (not self.returned) and timezone.now() > self.due_date

    def __str__(self):
        return f"Loan {self.book.title} to {self.borrower.username}"
