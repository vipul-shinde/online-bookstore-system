from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdminConfig(UserAdmin):
    list_display = ("first_name", "last_name", "email", "is_staff", 
                    "is_active", "is_suspended", "is_superuser", "password")

    fieldsets = (
        ("Account", {"fields": ("first_name", "last_name", "email", "password", "phone")}),
        ("Address", {"fields": ("street", "city", "state", "zip_code", "county", "country")}),
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


class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdminConfig)
admin.site.register(Cart, CartAdmin)
