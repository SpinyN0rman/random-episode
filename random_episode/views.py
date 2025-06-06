from django.shortcuts import render
from django.views import generic
from . import utils

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

class ContactView(generic.TemplateView):
    template_name = 'contact.html'