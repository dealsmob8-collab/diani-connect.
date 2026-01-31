from django import forms

from .models import Booking, Review, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "category",
            "area",
            "title",
            "description",
            "price_type",
            "price_amount",
            "gallery_image",
            "is_active",
        ]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["requested_date", "requested_time", "meeting_point", "mpesa_phone", "notes"]
        widgets = {
            "requested_date": forms.DateInput(attrs={"type": "date"}),
            "requested_time": forms.TimeInput(attrs={"type": "time"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
