import logging
import re
from typing import Optional

from apps.categories.models import Category

logger = logging.getLogger(__name__)

# Rule-based: (pattern_regex, category_name)
# Category names must exist in DB or be created on first use
CATEGORY_RULES = [
    (r"swiggy|zomato|dominos|pizza|foodpanda", "Food"),
    (r"uber|ola|rapido|lyft|taxi", "Travel"),
    (r"amazon|flipkart|myntra|ajio|meesho", "Shopping"),
    (r"netflix|prime\s*video|hotstar|spotify|youtube", "Entertainment"),
    (r"electricity|water|gas|broadband|wifi|jio|airtel|vodafone", "Utilities"),
    (r"rent|housing|emi|loan", "Rent & EMI"),
    (r"hospital|apollo|medicare|pharmacy", "Healthcare"),
    (r"petrol|fuel|shell|hp\s*petrol|indianoil", "Fuel"),
    (r"salary|cred|paytm|gpay|phonepe|transfer", "Transfer"),
]


class CategorizationService:
    _category_cache = {}

    @classmethod
    def get_or_create_category(cls, name: str) -> Optional[Category]:
        if not name:
            return None
        if name in cls._category_cache:
            return cls._category_cache[name]
        cat, _ = Category.objects.get_or_create(name=name, defaults={"description": f"Auto: {name}"})
        cls._category_cache[name] = cat
        return cat

    @classmethod
    def categorize_description(cls, description: str) -> Optional[Category]:
        if not description:
            return None
        text = (description or "").lower().strip()
        for pattern, category_name in CATEGORY_RULES:
            if re.search(pattern, text, re.IGNORECASE):
                return cls.get_or_create_category(category_name)
        return None
