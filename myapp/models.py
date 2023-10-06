from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user1 = models.CharField(max_length=50)
    pass1 = models.CharField(max_length=50)
    user_label = models.CharField(max_length=10)
    assign_by = models.IntegerField(null=True, blank=True)


class Book(models.Model):
    book_id = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    average_rating = models.CharField(max_length=300, null=True, blank=True)
    isbn = models.CharField(max_length=100, null=True, blank=True)
    isbn13 = models.CharField(max_length=100, null=True, blank=True)
    language_code = models.CharField(max_length=100, null=True, blank=True)
    pages = models.CharField(max_length=100, null=True, blank=True)
    rating_count = models.CharField(max_length=100, null=True, blank=True)
    text_reviews_count = models.CharField(max_length=100, null=True, blank=True)
    publication_date = models.DateField()
    publisher = models.CharField(max_length=100, null=True, blank=True)
    user_level = models.CharField(max_length=2, null=True, blank=True)
    issue_book = models.CharField(max_length=2, default="n")
    is_given = models.CharField(max_length=3, null=True, blank=True, default="no")
    is_return = models.CharField(max_length=3, null=True, blank=True, default="no")
    # import_count = models.PositiveIntegerField(default=0,null=True,blank=True)


class Member(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    outstanding_debt = models.DecimalField(max_digits=8, decimal_places=2)


class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
