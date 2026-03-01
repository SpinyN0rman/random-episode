from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField()


class EmailLoginForm(forms.Form):
    """Login form using email and password."""
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Please enter a correct email and password."
                )
        return self.cleaned_data

    def get_user(self):
        return getattr(self, "user_cache", None)


class SignupForm(UserCreationForm):
    """Signup form with email (no username)."""
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = ""  # keep username blank when using email-only
        if commit:
            user.save()
        return user