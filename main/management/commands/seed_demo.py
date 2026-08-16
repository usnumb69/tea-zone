from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from main.models import BotDetail, BotInfo, Category, Food, Product, Rooms


class Command(BaseCommand):
    help = "Create a local demo account and sample Tea Zone data."

    def handle(self, *args, **options):
        User = get_user_model()

        user, created = User.objects.get_or_create(
            username="ans",
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "role": 1,
            },
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.role = 1
        user.set_password("1")
        user.save()

        category, _ = Category.objects.get_or_create(name="Tea & Drinks")
        Food.objects.get_or_create(
            name="Classic Tea",
            defaults={"price": 15000, "available": True, "category": category},
        )
        Product.objects.get_or_create(
            name="Mineral Water",
            defaults={
                "price": 5000,
                "quantity": 20,
                "available": True,
                "category": category,
            },
        )
        Rooms.objects.get_or_create(number="101", defaults={"places": 4, "busy": False})
        Rooms.objects.get_or_create(number="102", defaults={"places": 6, "busy": False})

        BotInfo.objects.get_or_create(
            id=1,
            defaults={"text": "Welcome to Tea Zone!"},
        )
        BotDetail.objects.get_or_create(
            id=1,
            defaults={
                "text": "Tea Zone restaurant management demo.",
                "phone": "+998000000000",
                "lat": "41.3111",
                "lng": "69.2797",
            },
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo data is ready. Login: ans / 1 (local demo only)."
        ))
