from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='catalog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('borrow/<int:pk>/', views.request_borrow, name='request_borrow'),
    path('my-loans/', views.my_loans, name='my_loans'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('manage/borrow-requests/', views.borrow_requests, name='borrow_requests'),
]
