from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('lecteur','Lecteur'),('biblio','Bibliothécaire')], initial='lecteur')

    class Meta:
        model = User
        fields = ('username','email','password1','password2','first_name','last_name')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','description','authors','category','total_copies','available_copies','file','cover_url','is_new']
