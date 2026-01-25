from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("dashboard/bookings/", account_views.customer_bookings, name="customer_bookings"),
    path("dashboard/profile/", account_views.customer_profile, name="customer_profile"),
    path("provider/", account_views.provider_dashboard, name="provider_dashboard"),
    path("provider/profile/", account_views.provider_profile, name="provider_profile"),
    path("", include("marketplace.urls")),
    path("", include("blog.urls")),
]

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"
