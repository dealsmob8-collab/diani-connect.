from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/bookings/", views.customer_bookings, name="customer_bookings"),
    path("dashboard/profile/", views.customer_profile, name="customer_profile"),
    path("provider/", views.provider_dashboard, name="provider_dashboard"),
    path("provider/profile/", views.provider_profile, name="provider_profile"),
]
