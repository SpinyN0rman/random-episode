from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Manager for email-based User model."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with email as the login identifier."""
    username = models.CharField(max_length=150, blank=True, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """One-to-one profile for user (display name, timezone, etc.)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    display_name = models.CharField(max_length=150, blank=True)
    timezone = models.CharField(max_length=63, default='UTC')

    def __str__(self):
        return f"Profile for {self.user.email}"


class SavedShow(models.Model):
    """A show saved by a user for quick access."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_shows',
    )
    tvdb_show_id = models.IntegerField()
    show_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tvdb_show_id'],
                name='unique_user_saved_show',
            ),
        ]

    def __str__(self):
        return f"{self.show_name} (saved by {self.user.email})"


class RollHistory(models.Model):
    """Record of a random episode roll for a user."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='roll_history',
    )
    tvdb_show_id = models.IntegerField()
    show_name = models.CharField(max_length=255, blank=True)
    season_number = models.PositiveIntegerField()
    episode_number = models.PositiveIntegerField()
    episode_title = models.CharField(max_length=255, blank=True)
    rolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rolled_at']
        verbose_name_plural = 'Roll histories'

    def __str__(self):
        return f"{self.show_name} S{self.season_number}E{self.episode_number} at {self.rolled_at}"
