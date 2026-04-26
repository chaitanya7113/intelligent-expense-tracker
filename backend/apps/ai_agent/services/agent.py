import logging
import os

from django.utils import timezone

from apps.expenses.services import ExpenseService, AnalyticsService

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_TEMPLATE = """You are a smart, friendly personal finance assistant built into an Intelligent Expense Tracker app.
Your job is to help the user understand their spending, identify patterns, and make better financial decisions.

Here is a real-time snapshot of the user's finances for context:

--- Current month ({month_label}) ---
Total spending: {total_spending}
Number of expenses: {expense_count}

--- Spending by category (this month) ---
{category_breakdown}

--- Last 6 months trend ---
{monthly_trend}

--- 5 most recent expenses ---
{recent_expenses}
---

Guidelines:
- Answer concisely and helpfully in plain language.
- Reference the actual numbers above when relevant.
- If asked for advice, be specific and actionable.
- If you don't know something, say so honestly.
- Do not make up data that is not in the context above.
"""


def _build_system_prompt(user) -> str:
    now = timezone.now()
    year, month = now.year, now.month
    month_label = now.strftime("%B %Y")

    summary = AnalyticsService.monthly_summary(user, year=year, month=month)
    categories = AnalyticsService.category_breakdown(user, year=year, month=month)
    monthly_trend = AnalyticsService.monthly_comparison(user, months=6)
    recent_qs = ExpenseService.list_for_user(user)[:5]

    total_spending = summary.get("total_spending", 0)
    expense_count = summary.get("count", 0)

    if categories:
        cat_lines = "\n".join(
            f"  - {c['category_name']}: {c['total']:.2f} ({c['count']} expense{'s' if c['count'] != 1 else ''})"
            for c in categories
        )
    else:
        cat_lines = "  No category data available."

    if monthly_trend:
        trend_lines = "\n".join(
            f"  - {m['month_label']}: {m['total_spending']:.2f}"
            for m in reversed(monthly_trend)
        )
    else:
        trend_lines = "  No trend data available."

    if recent_qs:
        recent_lines = "\n".join(
            f"  - {e.date} | {e.category.name if e.category else 'Uncategorized'} | {e.amount:.2f}"
            + (f" | {e.description}" if e.description else "")
            for e in recent_qs
        )
    else:
        recent_lines = "  No recent expenses."

    return SYSTEM_PROMPT_TEMPLATE.format(
        month_label=month_label,
        total_spending=f"{total_spending:.2f}",
        expense_count=expense_count,
        category_breakdown=cat_lines,
        monthly_trend=trend_lines,
        recent_expenses=recent_lines,
    )


class AgentService:
    @staticmethod
    def chat(user, message: str, history: list) -> str:
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if api_key:
            return AgentService._openai_chat(user, message, history, api_key)
        return AgentService._fallback_chat(user, message)

    @staticmethod
    def _openai_chat(user, message: str, history: list, api_key: str) -> str:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            system_prompt = _build_system_prompt(user)

            messages = [{"role": "system", "content": system_prompt}]
            for entry in history:
                role = entry.get("role")
                content = entry.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=messages,
                max_tokens=512,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            logger.error("OpenAI chat error: %s", exc)
            return "Sorry, I encountered an error while processing your request. Please try again."

    @staticmethod
    def _fallback_chat(user, message: str) -> str:
        """Rule-based fallback when no OpenAI key is configured."""
        msg = message.lower()
        now = timezone.now()
        year, month = now.year, now.month

        if any(w in msg for w in ("total", "spend", "spent", "month", "how much")):
            summary = AnalyticsService.monthly_summary(user, year=year, month=month)
            total = summary.get("total_spending", 0)
            count = summary.get("count", 0)
            month_label = now.strftime("%B %Y")
            return (
                f"In {month_label} you spent a total of {total:.2f} across {count} expense(s)."
            )

        if any(w in msg for w in ("categor", "breakdown", "top", "most")):
            categories = AnalyticsService.category_breakdown(user, year=year, month=month)
            if not categories:
                return "No category data is available for this month."
            top = categories[:3]
            lines = ", ".join(
                f"{c['category_name']} ({c['total']:.2f})" for c in top
            )
            return f"Your top spending categories this month are: {lines}."

        if any(w in msg for w in ("trend", "comparison", "last", "previous", "month")):
            trend = AnalyticsService.monthly_comparison(user, months=6)
            if not trend:
                return "No monthly trend data is available."
            lines = ", ".join(
                f"{m['month_label']}: {m['total_spending']:.2f}" for m in reversed(trend)
            )
            return f"Your spending over the last 6 months: {lines}."

        if any(w in msg for w in ("tip", "advice", "save", "reduce", "cut", "budget")):
            categories = AnalyticsService.category_breakdown(user, year=year, month=month)
            if categories:
                top_cat = categories[0]
                return (
                    f"Your highest spending category is {top_cat['category_name']} "
                    f"({top_cat['total']:.2f}). Consider setting a budget for it to reduce spending."
                )
            return (
                "Track your expenses consistently and set a monthly budget for each category "
                "to keep your spending in check."
            )

        return (
            "I'm your expense assistant! You can ask me things like: "
            "'How much did I spend this month?', 'What are my top categories?', "
            "'Show me the spending trend', or 'Give me saving tips'."
        )
