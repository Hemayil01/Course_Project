from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, OneTimeCode

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'role', 'join_date', 'is_active', 'email_verified', 'phone_verified')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('-join_date',)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Course Info', {'fields': ('role','join_date','email_verified','phone_verified')}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','country','city','date_of_birth','phone_number')
    search_fields = ('user__username','user__email','country','city')
    list_filter = ('country','city')

@admin.register(OneTimeCode)
class OneTimeCodeAdmin(admin.ModelAdmin):
    list_display = ('user','purpose','code','is_used','expires_at','created_at')
    list_filter = ('purpose','is_used')
    search_fields = ('user__username','user__email','code')