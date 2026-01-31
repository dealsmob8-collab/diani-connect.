from django.urls import path

from . import views

urlpatterns = [
    path("services/", views.services_list, name="services_list"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("services/<slug:slug>/book/", views.booking_create, name="booking_create"),
    path("provider/services/", views.provider_services, name="provider_services"),
    path("provider/services/new/", views.service_create, name="service_create"),
    path("provider/services/<int:service_id>/edit/", views.service_update, name="service_update"),
    path("provider/services/<int:service_id>/delete/", views.service_delete, name="service_delete"),
    path("provider/bookings/", views.provider_bookings, name="provider_bookings"),
    path("provider/bookings/<int:booking_id>/<str:action>/", views.booking_action, name="booking_action"),
    path("reviews/<int:booking_id>/", views.review_create, name="review_create"),
]
