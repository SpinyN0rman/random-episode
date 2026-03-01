from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, SavedShow, RollHistory


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("-date_joined",)
    inlines = (ProfileInline,)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "timezone")
    search_fields = ("user__email", "display_name")


@admin.register(SavedShow)
class SavedShowAdmin(admin.ModelAdmin):
    list_display = ("user", "show_name", "tvdb_show_id", "created_at")
    list_filter = ("user",)
    search_fields = ("show_name", "user__email")


@admin.register(RollHistory)
class RollHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "show_name", "season_number", "episode_number", "rolled_at")
    list_filter = ("user",)
    search_fields = ("show_name", "user__email")
    date_hierarchy = "rolled_at"
