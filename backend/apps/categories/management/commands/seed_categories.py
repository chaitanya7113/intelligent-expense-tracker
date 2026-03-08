from django.core.management.base import BaseCommand
from apps.categories.models import Category

DEFAULTS = [
    ("Food", "Food and dining"),
    ("Travel", "Transport and travel"),
    ("Shopping", "Shopping and retail"),
    ("Entertainment", "Entertainment"),
    ("Utilities", "Bills and utilities"),
    ("Rent & EMI", "Rent and loan EMI"),
    ("Healthcare", "Health and medical"),
    ("Fuel", "Fuel and vehicle"),
    ("Transfer", "Transfers"),
]


class Command(BaseCommand):
    help = "Seed default categories"

    def handle(self, *args, **options):
        for name, desc in DEFAULTS:
            _, created = Category.objects.get_or_create(name=name, defaults={"description": desc})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
        self.stdout.write(self.style.SUCCESS("Done."))
