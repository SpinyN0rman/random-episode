from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("search/", views.search_results, name="search_results"),
    path("episode/", views.random_episode, name="random_episode"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact, name="contact")
]