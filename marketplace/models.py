from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Area(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    PRICE_FIXED = "fixed"
    PRICE_HOURLY = "hourly"
    PRICE_CHOICES = [
        (PRICE_FIXED, "Fixed"),
        (PRICE_HOURLY, "Hourly"),
    ]

    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    price_type = models.CharField(max_length=20, choices=PRICE_CHOICES)
    price_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gallery_image = models.ImageField(upload_to="services/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    @property
    def rating_average(self):
        ratings = Review.objects.filter(booking__service=self, is_hidden=False).values_list("rating", flat=True)
        ratings = list(ratings)
        if not ratings:
            return 0
        return round(sum(ratings) / len(ratings), 1)

    @property
    def review_count(self):
        return Review.objects.filter(booking__service=self, is_hidden=False).count()


class Booking(models.Model):
    STATUS_REQUESTED = "requested"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_REQUESTED, "Requested"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_bookings")
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provider_bookings")
    requested_date = models.DateField()
    requested_time = models.TimeField()
    meeting_point = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    mpesa_phone = models.CharField(max_length=30, blank=True)
    mpesa_reference = models.CharField(max_length=100, blank=True)
    mpesa_status = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.title} - {self.customer.username}"


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.booking.service.title}"

    @property
    def service(self):
        return self.booking.service


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
