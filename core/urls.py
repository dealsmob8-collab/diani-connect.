from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("how-it-works/", views.how_it_works, name="how_it_works"),
    path("become-a-provider/", views.become_provider, name="become_provider"),
    path("contact/", views.contact, name="contact"),
    path("moderation/", views.moderation, name="moderation"),
]
