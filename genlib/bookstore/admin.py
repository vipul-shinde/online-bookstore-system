from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdminConfig(UserAdmin):
    list_display = ("first_name", "last_name", "email", "is_staff", 
                    "is_active", "is_suspended", "is_superuser")

    fieldsets = (
        ("Account", {"fields": ("first_name", "last_name", "email", "password", "phone")}),
        ("Address", {"fields": ("street", "city", "state", "zip_code")}),
        ("Payment", {"fields": ("card_name", "card_num", "card_exp", "card_cvv")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_suspended")}),
        ("Promotions", {"fields": ("receive_promotions",)}),
    )

    add_fieldsets = (
        ("Account", {"fields": ("first_name", "last_name", "email", "password", "phone")}),
        ("Address", {"fields": ("street", "city", "state", "zip_code")}),
        ("Payment", {"fields": ("card_name", "card_num", "card_exp", "card_cvv")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_suspended")}),
        ("Promotions", {"fields": ("receive_promotions")}),
    )

    ordering = ("email",)


class BookAdmin(admin.ModelAdmin):
    list_display = ("isbn", "category", "title", "image_path",
                    "edition", "publisher", "publication_year",
                    "author", "stock", "cost", "rating")

# Register your models here.
admin.site.register(User, UserAdminConfig)
admin.site.register(Book, BookAdmin)