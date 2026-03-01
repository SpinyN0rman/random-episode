from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import EmailMessage
from . import utils
from .forms import ContactForm, EmailLoginForm, SignupForm
from .models import Profile, SavedShow, RollHistory
import os

class HomePageView(generic.TemplateView):
    template_name = 'home.html'


def search_results(request):
    results = "None"
    query = ""
    saved_show_ids = set()
    if request.user.is_authenticated:
        saved_show_ids = set(
            SavedShow.objects.filter(user=request.user).values_list("tvdb_show_id", flat=True)
        )
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query != "":
            results = utils.tvdb_search(query)
    return render(
        request,
        "search_results.html",
        {"results": results, "query": query, "saved_show_ids": saved_show_ids},
    )

def random_episode(request):
    episode = "None"
    show = "None"
    eng_name = "None"
    eng_episode_deets = "None"
    show_id = request.GET.get("show_id", "") if request.method == "GET" else ""
    if request.method == "GET" and show_id != "":
        show, episode, eng_name, eng_episode_deets = utils.tvdb_episodes(show_id)
        if request.user.is_authenticated and episode != "None":
            episode_title = ""
            if isinstance(eng_episode_deets, dict):
                episode_title = eng_episode_deets.get("name", "")
            elif isinstance(episode, dict):
                episode_title = episode.get("name", "")
            RollHistory.objects.create(
                user=request.user,
                tvdb_show_id=int(show_id),
                show_name=eng_name if eng_name != "None" else "",
                season_number=episode.get("seasonNumber", 0) if isinstance(episode, dict) else 0,
                episode_number=episode.get("number", 0) if isinstance(episode, dict) else 0,
                episode_title=episode_title,
            )
    is_saved = False
    if request.user.is_authenticated and show_id:
        try:
            is_saved = SavedShow.objects.filter(
                user=request.user, tvdb_show_id=int(show_id)
            ).exists()
        except (ValueError, TypeError):
            pass
    return render(
        request,
        "random_episode.html",
        {
            "show": show,
            "episode": episode,
            "eng_name": eng_name,
            "eng_episode_deets": eng_episode_deets,
            "show_id": show_id,
            "is_saved": is_saved,
        },
    )


class AboutView(generic.TemplateView):
    template_name = 'about.html'


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        message_body = f"New contact form submission from: {name}\n\n" \
                        f"Email: {email}\n" \
                        f"Their message:\n\n" \
                        f"{subject}\n" \
                        f"{message}"

        email_message = EmailMessage(f"New Random Episode Form: {subject}",
                                      message_body, to=[os.getenv("ADMIN_EMAIL")])

        email_message.send()

        messages.success(request, "Form submitted successfully, thank you!")
        return redirect("contact")
    return render(request, "contact.html", {"form": form})


# --- Auth views (email-based login) ---

class EmailLoginView(LoginView):
    """Login using email and password."""
    form_class = EmailLoginForm
    template_name = "registration/login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        messages.success(request, "Account created. You are now logged in.")
        return redirect("home")
    return render(request, "registration/signup.html", {"form": form})


# --- Saved shows and roll history ---

@login_required
def saved_shows_list(request):
    """List the current user's saved shows."""
    saved = SavedShow.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "saved_shows.html", {"saved_shows": saved})


def save_show(request):
    """Add a show to the user's saved list (POST: show_id, show_name)."""
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("home")
    show_id = request.POST.get("show_id")
    show_name = request.POST.get("show_name", "")
    if show_id:
        try:
            SavedShow.objects.get_or_create(
                user=request.user,
                tvdb_show_id=int(show_id),
                defaults={"show_name": show_name[:255]},
            )
            messages.success(request, "Show saved.")
        except (ValueError, TypeError):
            pass
    next_url = request.GET.get("next") or request.POST.get("next") or request.META.get("HTTP_REFERER")
    return redirect(next_url) if next_url else redirect("home")


def unsave_show(request):
    """Remove a show from the user's saved list (POST: show_id)."""
    if not request.user.is_authenticated or request.method != "POST":
        return redirect("home")
    show_id = request.POST.get("show_id")
    if show_id:
        try:
            SavedShow.objects.filter(user=request.user, tvdb_show_id=int(show_id)).delete()
            messages.success(request, "Show removed from saved list.")
        except (ValueError, TypeError):
            pass
    next_url = request.GET.get("next") or request.POST.get("next") or request.META.get("HTTP_REFERER")
    return redirect(next_url) if next_url else redirect("home")


@login_required
def roll_history_list(request):
    """List the current user's roll history."""
    history = RollHistory.objects.filter(user=request.user)[:50]
    return render(request, "roll_history.html", {"rolls": history})