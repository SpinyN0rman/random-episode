from django.shortcuts import render
from django.views import generic
from . import utils

class HomePageView(generic.TemplateView):
    template_name = 'home.html'


def search_results(request):
    results = "None"
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query != "":
            results = utils.tvdb_search(query)
    return render(request, "search_results.html", {'results': results})


class RandomEpisodeView(generic.TemplateView):
    template_name = 'random_episode.html'

class AboutView(generic.TemplateView):
    template_name = 'about.html'

class ContactView(generic.TemplateView):
    template_name = 'contact.html'