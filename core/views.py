from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import ProviderProfile
from blog.models import BlogPost
from marketplace.models import Area, Category, ContactMessage, Review, Service


def home(request):
    categories = Category.objects.all()[:6]
    areas = Area.objects.all()
    featured_services = Service.objects.filter(is_active=True)[:6]
    featured_providers = ProviderProfile.objects.filter(verified=True)[:4]
    latest_reviews = Review.objects.filter(is_hidden=False).order_by("-created_at")[:3]
    posts = BlogPost.objects.order_by("-published_at")[:3]
    return render(
        request,
        "core/home.html",
        {
            "categories": categories,
            "areas": areas,
            "featured_services": featured_services,
            "featured_providers": featured_providers,
            "latest_reviews": latest_reviews,
            "posts": posts,
        },
    )


def how_it_works(request):
    return render(request, "core/how_it_works.html")


def become_provider(request):
    return render(request, "core/become_provider.html")


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            message=request.POST.get("message", ""),
        )
        messages.success(request, "Thanks! We will reach out shortly.")
        return redirect("contact")
    return render(request, "core/contact.html")


@login_required
def moderation(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Admins only")
    providers = ProviderProfile.objects.select_related("user").order_by("business_name")
    services = Service.objects.order_by("-created_at")
    reviews = Review.objects.order_by("-created_at")

    if request.method == "POST":
        action = request.POST.get("action")
        object_id = request.POST.get("object_id")
        if action == "toggle_verified":
            provider = get_object_or_404(ProviderProfile, id=object_id)
            provider.verified = not provider.verified
            provider.save()
            messages.success(request, "Provider verified status updated.")
        elif action == "toggle_approved":
            provider = get_object_or_404(ProviderProfile, id=object_id)
            provider.is_approved = not provider.is_approved
            provider.save()
            messages.success(request, "Provider approval updated.")
        elif action == "toggle_service":
            service = get_object_or_404(Service, id=object_id)
            service.is_active = not service.is_active
            service.save()
            messages.success(request, "Service status updated.")
        elif action == "toggle_review":
            review = get_object_or_404(Review, id=object_id)
            review.is_hidden = not review.is_hidden
            review.save()
            messages.success(request, "Review status updated.")
        return redirect("moderation")

    return render(
        request,
        "core/moderation.html",
        {"providers": providers, "services": services, "reviews": reviews},
    )


def custom_404(request, exception):
    return render(request, "core/404.html", status=404)


def custom_500(request):
    return render(request, "core/500.html", status=500)
