from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile

from .forms import BookingForm, ReviewForm, ServiceForm
from .models import Area, Booking, Category, Review, Service


def services_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category")
    area_id = request.GET.get("area")

    services = Service.objects.filter(is_active=True)
    if query:
        services = services.filter(title__icontains=query)
    if category_id:
        services = services.filter(category_id=category_id)
    if area_id:
        services = services.filter(area_id=area_id)

    paginator = Paginator(services.order_by("-created_at"), 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "services": page_obj,
        "categories": Category.objects.all(),
        "areas": Area.objects.all(),
        "query": query,
        "selected_category": category_id,
        "selected_area": area_id,
    }

    if request.headers.get("HX-Request"):
        return render(request, "marketplace/partials/services_list.html", context)

    return render(request, "marketplace/services.html", context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    booking_form = BookingForm()
    review_form = ReviewForm()
    reviews = Review.objects.filter(booking__service=service, is_hidden=False).order_by("-created_at")
    eligible_bookings = []
    if request.user.is_authenticated:
        eligible_bookings = Booking.objects.filter(
            service=service,
            customer=request.user,
            status=Booking.STATUS_COMPLETED,
        ).exclude(review__isnull=False)

    return render(
        request,
        "marketplace/service_detail.html",
        {
            "service": service,
            "booking_form": booking_form,
            "review_form": review_form,
            "reviews": reviews,
            "eligible_bookings": eligible_bookings,
        },
    )


@login_required
def service_create(request):
    if request.user.profile.role != Profile.ROLE_PROVIDER:
        return HttpResponseForbidden("Providers only")
    if hasattr(request.user, "providerprofile") and not request.user.providerprofile.is_approved:
        return HttpResponseForbidden("Provider account pending approval")
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            service.save()
            messages.success(request, "Service created.")
            return redirect("provider_services")
    else:
        form = ServiceForm()
    return render(request, "marketplace/provider/service_form.html", {"form": form, "title": "New Service"})


@login_required
def service_update(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider=request.user)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated.")
            return redirect("provider_services")
    else:
        form = ServiceForm(instance=service)
    return render(request, "marketplace/provider/service_form.html", {"form": form, "title": "Edit Service"})


@login_required
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id, provider=request.user)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service removed.")
        return redirect("provider_services")
    return render(request, "marketplace/provider/service_delete.html", {"service": service})


@login_required
def provider_services(request):
    services = Service.objects.filter(provider=request.user).order_by("-created_at")
    return render(request, "marketplace/provider/services.html", {"services": services})


@login_required
def provider_bookings(request):
    bookings = Booking.objects.filter(provider=request.user).order_by("-created_at")
    return render(request, "marketplace/provider/bookings.html", {"bookings": bookings})


@login_required
def booking_action(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id, provider=request.user)
    if request.method != "POST":
        return HttpResponseForbidden("Invalid method")
    status_map = {
        "accept": Booking.STATUS_ACCEPTED,
        "decline": Booking.STATUS_DECLINED,
        "complete": Booking.STATUS_COMPLETED,
    }
    if action not in status_map:
        return HttpResponseForbidden("Invalid action")
    booking.status = status_map[action]
    booking.save()

    if request.headers.get("HX-Request"):
        return render(request, "marketplace/partials/booking_row.html", {"booking": booking})
    messages.success(request, "Booking updated.")
    return redirect("provider_bookings")


@login_required
def booking_create(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    if request.user.profile.role != Profile.ROLE_CUSTOMER:
        return HttpResponseForbidden("Customers only")
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.customer = request.user
            booking.provider = service.provider
            booking.save()
            if request.headers.get("HX-Request"):
                return render(request, "marketplace/partials/booking_success.html", {"booking": booking})
            messages.success(request, "Booking requested.")
            return redirect("dashboard")
    else:
        form = BookingForm()
    return render(request, "marketplace/booking_form.html", {"form": form, "service": service})


@login_required
def review_create(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status != Booking.STATUS_COMPLETED:
        return HttpResponseForbidden("Booking not completed")
    if hasattr(booking, "review"):
        return HttpResponseForbidden("Review already exists")
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            if request.headers.get("HX-Request"):
                return render(request, "marketplace/partials/review_item.html", {"review": review})
            messages.success(request, "Review submitted.")
            return redirect("service_detail", slug=booking.service.slug)
    return redirect("service_detail", slug=booking.service.slug)
