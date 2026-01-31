from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Profile, ProviderProfile
from blog.models import BlogPost
from marketplace.models import Area, Booking, Category, Review, Service


class Command(BaseCommand):
    help = "Seed demo data for Diani Connect"

    def handle(self, *args, **options):
        areas = ["Diani", "Ukunda", "Tiwi", "Msambweni", "Kwale Town"]
        area_objs = [Area.objects.get_or_create(name=name)[0] for name in areas]

        categories = [
            "Plumbing",
            "Cleaning",
            "Events & Decor",
            "Tutors/Learning",
            "Handyman",
            "Photography",
        ]
        category_objs = []
        for name in categories:
            category_objs.append(Category.objects.get_or_create(name=name, slug=name.lower().replace(" ", "-"))[0])

        provider_user, _ = User.objects.get_or_create(username="provider_demo", defaults={"email": "provider@demo.com"})
        provider_user.set_password("provider123")
        provider_user.save()
        provider_user.profile.role = Profile.ROLE_PROVIDER
        provider_user.profile.phone = "+254700111222"
        provider_user.profile.area = area_objs[0]
        provider_user.profile.save()

        provider_profile, _ = ProviderProfile.objects.get_or_create(
            user=provider_user,
            defaults={
                "business_name": "Diani Sparkle Cleaning",
                "bio": "Professional cleaning services for homes and villas.",
                "is_approved": True,
                "verified": True,
            },
        )

        customer_user, _ = User.objects.get_or_create(username="customer_demo", defaults={"email": "customer@demo.com"})
        customer_user.set_password("customer123")
        customer_user.save()
        customer_user.profile.role = Profile.ROLE_CUSTOMER
        customer_user.profile.phone = "+254700333444"
        customer_user.profile.area = area_objs[1]
        customer_user.profile.save()

        admin_user, _ = User.objects.get_or_create(username="admin_demo", defaults={"email": "admin@demo.com", "is_staff": True})
        admin_user.set_password("admin123")
        admin_user.is_superuser = True
        admin_user.save()

        if not Service.objects.filter(provider=provider_user).exists():
            Service.objects.create(
                provider=provider_user,
                category=category_objs[1],
                area=area_objs[0],
                title="Villa Deep Cleaning",
                description="Full villa deep cleaning including kitchens and outdoor spaces.",
                price_type=Service.PRICE_FIXED,
                price_amount=3500,
            )
            Service.objects.create(
                provider=provider_user,
                category=category_objs[0],
                area=area_objs[1],
                title="Emergency Plumbing Repair",
                description="On-call plumbing repairs for leaks and urgent fixes.",
                price_type=Service.PRICE_HOURLY,
                price_amount=1200,
            )

        service = Service.objects.filter(provider=provider_user).first()
        booking, _ = Booking.objects.get_or_create(
            service=service,
            customer=customer_user,
            provider=provider_user,
            defaults={
                "requested_date": timezone.now().date(),
                "requested_time": timezone.now().time(),
                "meeting_point": "Diani Beach Road",
                "notes": "Please bring eco-friendly supplies.",
                "status": Booking.STATUS_COMPLETED,
            },
        )

        if not hasattr(booking, "review"):
            Review.objects.create(booking=booking, rating=5, comment="Amazing service and friendly team!")

        if not BlogPost.objects.exists():
            BlogPost.objects.create(
                title="Top 5 Tips for Hiring Service Providers in Diani",
                excerpt="Learn how to choose reliable pros for your home and business.",
                body="Always check reviews, compare pricing, and confirm availability before booking.",
                published_at=timezone.now(),
            )
            BlogPost.objects.create(
                title="Preparing Your Home for a Deep Clean",
                excerpt="Simple steps to help cleaning teams work faster.",
                body="Declutter and communicate priority areas for the best results.",
                published_at=timezone.now(),
            )

        self.stdout.write(self.style.SUCCESS("Demo data created."))
