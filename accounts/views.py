from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render

from marketplace.models import Booking

from .forms import LoginForm, SignUpForm
from .models import Profile


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    next_page = "/"


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Diani Connect!")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.role == Profile.ROLE_PROVIDER:
        return redirect("provider_dashboard")
    bookings = Booking.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "accounts/dashboard.html", {"bookings": bookings})


@login_required
def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "accounts/bookings.html", {"bookings": bookings})


@login_required
def customer_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        profile.phone = request.POST.get("phone", "")
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("customer_profile")
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required
def provider_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != Profile.ROLE_PROVIDER:
        return redirect("dashboard")
    bookings = Booking.objects.filter(provider=request.user).order_by("-created_at")[:5]
    services = request.user.service_set.order_by("-created_at")[:5]
    return render(
        request,
        "accounts/provider_dashboard.html",
        {"bookings": bookings, "services": services},
    )


@login_required
def provider_profile(request):
    profile = request.user.profile
    if profile.role != Profile.ROLE_PROVIDER:
        return redirect("dashboard")
    provider_profile = request.user.providerprofile
    if request.method == "POST":
        provider_profile.business_name = request.POST.get("business_name", provider_profile.business_name)
        provider_profile.bio = request.POST.get("bio", provider_profile.bio)
        provider_profile.save()
        messages.success(request, "Provider profile updated.")
        return redirect("provider_profile")
    return render(request, "accounts/provider_profile.html", {"provider_profile": provider_profile})
