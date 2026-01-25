from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from marketplace.models import Area

from .models import Profile, ProviderProfile


class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        (Profile.ROLE_CUSTOMER, "Customer"),
        (Profile.ROLE_PROVIDER, "Provider"),
    ]

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    phone = forms.CharField(required=False)
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False)
    business_name = forms.CharField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = user.profile
            profile.role = self.cleaned_data["role"]
            profile.phone = self.cleaned_data.get("phone", "")
            if self.cleaned_data.get("area"):
                profile.area = self.cleaned_data["area"]
            profile.save()
            if profile.role == Profile.ROLE_PROVIDER:
                ProviderProfile.objects.create(
                    user=user,
                    business_name=self.cleaned_data.get("business_name") or f"{user.username} Services",
                    bio=self.cleaned_data.get("bio", ""),
                )
        return user


class LoginForm(AuthenticationForm):
    pass
