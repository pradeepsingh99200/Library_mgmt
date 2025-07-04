from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Transaction
from .forms import BookForm, MemberForm
import requests
from datetime import date
from decimal import Decimal

# Book CRUD

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save()
        book.available_stock = book.stock
        book.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form})

# Member CRUD

def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def member_create(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('member_list')
    return render(request, 'member_form.html', {'form': form})

# Issue Book

def transaction_list(request):
    transactions = Transaction.objects.select_related('book', 'member').all().order_by('-issue_date')
    return render(request, 'transaction_list.html', {'transactions': transactions})


def issue_book(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        member_id = request.POST['member_id']
        book = get_object_or_404(Book, id=book_id)
        member = get_object_or_404(Member, id=member_id)

        if book.available_stock > 0 and member.total_debt <= 500:
            Transaction.objects.create(book=book, member=member)
            book.available_stock -= 1
            book.save()
            return redirect('transaction_list')
    books = Book.objects.all()
    members = Member.objects.all()
    return render(request, 'issue_book.html', {'books': books, 'members': members})

# Return Book

def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if not transaction.is_returned:
        transaction.return_date = date.today()
        transaction.rent_fee = Decimal('50.00')
        transaction.is_returned = True
        transaction.save()

        transaction.book.available_stock += 1
        transaction.book.save()

        transaction.member.total_debt += transaction.rent_fee
        transaction.member.save()
    return redirect('transaction_list')

# Import Books from Frappe API

def import_books(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        num_books = int(request.POST.get('num_books', '10'))
        page = 1
        imported = 0

        while imported < num_books:
            response = requests.get(f'https://frappe.io/api/method/frappe-library?page={page}&title={title}')
            data = response.json()['message']
            if not data:
                break
            for item in data:
                if imported >= num_books:
                    break
                Book.objects.create(
                    title=item['title'],
                    authors=item['authors'], 
                    isbn=item['isbn'],
                    publisher=item['publisher'],
                    num_pages=int(item['num_pages'] or 0),
                    stock=5,
                    available_stock=5
                )
                imported += 1
            page += 1
        return redirect('book_list')
    return render(request, 'import_books.html')
