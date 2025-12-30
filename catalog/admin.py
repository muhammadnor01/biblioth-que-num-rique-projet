from django.contrib import admin
from .models import Profile, Category, Author, Book, Reservation, Loan
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Category)
admin.site.register(Author)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','category','available_copies','total_copies','is_new')
    list_filter = ('category','is_new')

admin.site.register(Reservation)
admin.site.register(Loan)
