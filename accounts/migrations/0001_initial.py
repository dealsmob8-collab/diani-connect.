# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("marketplace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "role",
                    models.CharField(
                        choices=[("customer", "Customer"), ("provider", "Provider"), ("admin", "Admin")],
                        default="customer",
                        max_length=20,
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("avatar", models.ImageField(blank=True, null=True, upload_to="avatars/")),
                (
                    "area",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="marketplace.area"),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProviderProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(max_length=200)),
                ("bio", models.TextField(blank=True)),
                ("is_approved", models.BooleanField(default=False)),
                ("verified", models.BooleanField(default=False)),
                ("services_count", models.PositiveIntegerField(default=0)),
                ("rating_avg", models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                (
                    "plan_type",
                    models.CharField(
                        choices=[("free", "Free"), ("premium", "Premium")],
                        default="free",
                        max_length=20,
                    ),
                ),
                ("plan_expires", models.DateField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]
