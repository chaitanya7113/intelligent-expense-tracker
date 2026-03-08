import csv
import io
import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Optional
from dateutil import parser as date_parser

from django.conf import settings
from apps.transactions.models import TransactionSource, Transaction
from apps.transactions.services.categorization import CategorizationService

logger = logging.getLogger(__name__)


def _normalize_date(value: str) -> Optional[datetime]:
    if not value or not value.strip():
        return None
    try:
        parsed = date_parser.parse(value.strip())
        return parsed.date() if hasattr(parsed, "date") else parsed
    except Exception:
        return None


def _normalize_amount(value: str) -> Optional[Decimal]:
    if value is None or value == "":
        return None
    s = str(value).strip().replace(",", "").replace(" ", "")
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    if s.startswith("-") or s.startswith("+"):
        pass
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def _detect_debit_credit(amount: Decimal, debit_col: Optional[str], credit_col: Optional[str],
                         row: dict) -> str:
    if debit_col and debit_col in row and row[debit_col]:
        d = _normalize_amount(str(row[debit_col]))
        if d is not None and d > 0:
            return Transaction.TransactionType.DEBIT
    if credit_col and credit_col in row and row[credit_col]:
        c = _normalize_amount(str(row[credit_col]))
        if c is not None and c > 0:
            return Transaction.TransactionType.CREDIT
    return Transaction.TransactionType.DEBIT if amount < 0 else Transaction.TransactionType.CREDIT


def _guess_column_mapping(headers: List[str]) -> dict:
    headers_lower = [h.lower().strip() for h in headers]
    mapping = {"date": None, "description": None, "amount": None, "debit": None, "credit": None}
    for i, h in enumerate(headers_lower):
        if h in ("date", "transaction date", "value date", "posting date"):
            mapping["date"] = headers[i]
        elif h in ("description", "particulars", "narration", "remarks", "details"):
            mapping["description"] = headers[i]
        elif h in ("amount", "transaction amount", "balance"):
            mapping["amount"] = headers[i]
        elif h in ("debit", "withdrawal", "dr"):
            mapping["debit"] = headers[i]
        elif h in ("credit", "deposit", "cr"):
            mapping["credit"] = headers[i]
    if not mapping["date"] and any("date" in x for x in headers_lower):
        for i, h in enumerate(headers_lower):
            if "date" in h:
                mapping["date"] = headers[i]
                break
    if not mapping["description"] and any("desc" in x or "part" in x or "nar" in x for x in headers_lower):
        for i, h in enumerate(headers_lower):
            if "desc" in h or "part" in h or "nar" in h or "detail" in h:
                mapping["description"] = headers[i]
                break
    return mapping


class StatementParserService:
    @staticmethod
    def parse_csv(
        file_content: bytes | str,
        user,
        source: Optional[TransactionSource] = None,
        source_name: str = "Uploaded Statement",
    ) -> List[Transaction]:
        if isinstance(file_content, bytes):
            content = file_content.decode("utf-8", errors="replace")
        else:
            content = file_content
        reader = csv.DictReader(io.StringIO(content))
        headers = reader.fieldnames or []
        mapping = _guess_column_mapping(list(headers))
        date_col = mapping["date"]
        desc_col = mapping["description"]
        amount_col = mapping["amount"]
        debit_col = mapping["debit"]
        credit_col = mapping["credit"]

        if not source and user:
            source = TransactionSource.objects.create(
                user=user, name=source_name, source_type=TransactionSource.SourceType.BANK
            )

        created = []
        for row in reader:
            date_val = _normalize_date(row.get(date_col or "", ""))
            desc_val = (row.get(desc_col or "", "") or "").strip() or "Unknown"
            amt = _normalize_amount(row.get(amount_col or "", ""))
            if amt is None and (debit_col or credit_col):
                deb = _normalize_amount(row.get(debit_col or "", ""))
                cred = _normalize_amount(row.get(credit_col or "", ""))
                if deb is not None and (cred is None or cred == 0):
                    amt = deb
                elif cred is not None:
                    amt = cred
            if date_val is None or amt is None:
                continue
            if amt == 0:
                continue
            # If single amount column: negative often = credit (inflow), positive = debit (outflow)
            if (debit_col and row.get(debit_col)) or (credit_col and row.get(credit_col)):
                tx_type = _detect_debit_credit(amt, debit_col, credit_col, row)
            else:
                tx_type = Transaction.TransactionType.CREDIT if amt < 0 else Transaction.TransactionType.DEBIT
            amount_abs = abs(amt)
            category = CategorizationService.categorize_description(desc_val)
            t = Transaction.objects.create(
                user=user,
                source=source,
                date=date_val,
                description=desc_val[:500],
                amount=amount_abs,
                transaction_type=tx_type,
                category=category,
                raw_data=dict(row),
            )
            created.append(t)
        logger.info("Parsed %s transactions from CSV for user %s", len(created), user.id)
        return created
