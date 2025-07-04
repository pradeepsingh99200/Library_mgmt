from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.TextField()
    isbn = models.CharField(max_length=13, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    num_pages = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    available_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    total_debt = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.member.name}"