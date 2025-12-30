from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Reservation, Loan, Profile
from django.contrib.auth import login
from .forms import SignUpForm, BookForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    new_books = Book.objects.filter(is_new=True).order_by('-created_at')[:6]
    recent = Book.objects.order_by('-created_at')[:6]
    return render(request, 'catalog/index.html', {'new_books': new_books, 'recent': recent})

def book_list(request):
    q = request.GET.get('q','')
    if q:
        books = Book.objects.filter(title__icontains=q) | Book.objects.filter(description__icontains=q)
    else:
        books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books, 'q': q})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        role = request.POST.get('role','lecteur')
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, "Compte créé avec succès.")
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'catalog/signup.html', {'form': form})

@login_required
def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    return render(request, 'catalog/dashboard.html', {'profile': profile})

@login_required
def request_borrow(request, pk):
    book = get_object_or_404(Book, pk=pk)
    active_loans = Loan.objects.filter(borrower=request.user, returned=False).count()
    if active_loans >= 3:
        messages.error(request, "Vous avez atteint le maximum d’emprunts (3).")
        return redirect('book_detail', pk=pk)

    if book.available_copies <= 0:
        Reservation.objects.create(book=book, user=request.user)
        messages.info(request, "Réservation enregistrée.")
        return redirect('book_detail', pk=pk)

    due = timezone.now() + timedelta(days=14)
    Loan.objects.create(book=book, borrower=request.user, due_date=due)
    book.available_copies -= 1
    book.save()
    messages.success(request, "Emprunt réussi !")
    return redirect('my_loans')

@login_required
def my_loans(request):
    loans = Loan.objects.filter(borrower=request.user)
    return render(request, 'catalog/my_loans.html', {'loans': loans})

@login_required
def my_reservations(request):
    reserves = Reservation.objects.filter(user=request.user, active=True)
    return render(request, 'catalog/borrow_requests.html', {'reservations': reserves})

def is_biblio(user):
    return hasattr(user, 'profile') and user.profile.role in ('biblio','admin')

@login_required
@user_passes_test(is_biblio)
def borrow_requests(request):
    loans = Loan.objects.filter(returned=False).order_by('due_date')
    reservations = Reservation.objects.filter(active=True).order_by('-reserved_at')
    return render(request, 'catalog/borrow_requests.html', {'loans': loans, 'reservations': reservations})
