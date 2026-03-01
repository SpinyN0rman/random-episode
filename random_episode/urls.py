from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("search/", views.search_results, name="search_results"),
    path("episode/", views.random_episode, name="random_episode"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact"),
    path("saved-shows/", views.saved_shows_list, name="saved_shows"),
    path("saved-shows/save/", views.save_show, name="save_show"),
    path("saved-shows/unsave/", views.unsave_show, name="unsave_show"),
    path("history/", views.roll_history_list, name="roll_history"),
]