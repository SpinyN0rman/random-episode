from django.shortcuts import render, redirect
from django.views import generic
from . import utils
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import os


def home(request):
    recents_cookie = [r for r in request.COOKIES.get('recents', '').split(',') if r.isdigit()]
    recent_shows = utils.recents(recents_cookie)
    if 'trending' not in request.COOKIES:
        trending_shows = utils.trending()
        trending_string = utils.trending_to_string(trending_shows)
        response = render(request, "home.html", {'trending_shows': trending_shows, 'recent_shows': recent_shows})
        response.set_cookie('trending', trending_string, max_age=60 * 60 * 12)
        return response
    else:
        trending_cookie = request.COOKIES.get('trending', '')
        trending_shows = utils.trending_from_string(trending_cookie)
        response = render(request, "home.html", {'trending_shows': trending_shows, 'recent_shows':recent_shows})
        return response


def search_results(request):
    results = "None"
    query = ""
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query != "":
            results = utils.tvdb_search(query)
    return render(request, "search_results.html", {'results': results, 'query': query})


def random_episode(request):
    recents_cookie = [r for r in request.COOKIES.get('recents', '').split(',') if r.isdigit()]
    episode = "None"
    show = "None"
    eng_name = "None"
    eng_episode_deets = "None"
    show_id = ""
    if request.method == "GET":
        show_id = request.GET.get("show_id", "")
        season_id = request.GET.get("season_id", "")
        episode_num = request.GET.get("episode_num", "")

        if show_id.isdigit():
            recents_cookie = [show_id] + [r for r in recents_cookie if r != show_id]
            recents_cookie = recents_cookie[:8]

        if season_id != "" and episode_num != "":
            show, episode, eng_name, eng_episode_deets = utils.tvdb_episode_load(show_id, season_id, episode_num)
        elif show_id != "":
            season_id, episode_num = utils.tvdb_episodes(show_id)
            url = f"{request.path}?{request.GET.urlencode()}&season_id={season_id}&episode_num={episode_num}"
            response = redirect(url)
            response.set_cookie('recents', ','.join(recents_cookie), max_age=60 * 60 * 24 * 365)
            return response

    response = render(request, "random_episode.html", {
        'show_id': show_id,
        'show': show,
        'episode': episode,
        'eng_name': eng_name,
        'eng_episode_deets': eng_episode_deets,
        'recents': recents_cookie,
    })
    response.set_cookie('recents', ','.join(recents_cookie), max_age=60 * 60 * 24 * 365)
    return response


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