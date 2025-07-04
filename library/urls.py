from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/new/', views.book_create, name='book_create'),
    path('members/', views.member_list, name='member_list'),
    path('member/new/', views.member_create, name='member_create'),
    path('issue/', views.issue_book, name='issue_book'),
    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('import/', views.import_books, name='import_books'),
    path('transactions/', views.transaction_list, name='transaction_list'),

]