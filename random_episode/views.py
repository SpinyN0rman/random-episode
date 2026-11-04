from django.shortcuts import render, redirect
from django.views import generic
from . import utils
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import os

class HomePageView(generic.TemplateView):
    template_name = 'home.html'


def search_results(request):
    results = "None"
    query = ""
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query != "":
            results = utils.tvdb_search(query)
    return render(request, "search_results.html", {'results': results, 'query': query})

def random_episode(request):
    episode = "None"
    show = "None"
    eng_name = "None"
    eng_episode_deets = "None"
    show_id = ""
    if request.method == "GET":
        show_id = request.GET.get("show_id", "")
        season_id = request.GET.get("season_id", "")
        episode_num = request.GET.get("episode_num", "")
        if season_id != "" and episode_num != "":
            show, episode, eng_name, eng_episode_deets = utils.tvdb_episode_load(show_id, season_id, episode_num)
        elif show_id != "":
            season_id, episode_num = utils.tvdb_episodes(show_id)
            url = f"{request.path}?{request.GET.urlencode()}&season_id={season_id}&episode_num={episode_num}"
            return redirect(url)
    return render(request, "random_episode.html", {'show_id': show_id, 'show': show, 'episode': episode, 'eng_name': eng_name, 'eng_episode_deets': eng_episode_deets})


class AboutView(generic.TemplateView):
    template_name = 'about.html'


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
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
    return render(request, "contact.html")