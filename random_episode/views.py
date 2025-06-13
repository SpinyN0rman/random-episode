from django.shortcuts import render
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
    if request.method == "GET":
        show_id = request.GET.get("show_id", "")
        if show_id != "":
            show, episode = utils.tvdb_episodes(show_id)
    return render(request, "random_episode.html", {'show': show, 'episode': episode})


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