from datetime import datetime

from services.api.analyses.schemas.lifeline.constants import DAYS_PER_MONTH


def months_between(start: datetime, end: datetime) -> int:
    """Whole months between two datetimes (never negative)."""
    months = (end.year - start.year) * 12 + (end.month - start.month)
    return max(months, 0)


def span_months(start: datetime, end: datetime) -> float:
    """Day-precise month span used for proportional timeline heights."""
    return max((end - start).days, 0) / DAYS_PER_MONTH


def now_like(sample: datetime) -> datetime:
    """Current time matching the sample's tz-awareness (naive here)."""
    return datetime.now(sample.tzinfo)


def duration_label(months: int) -> str:
    """Human duration like "11 мес" or "1 г 2 мес"."""
    years, rest = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} г")
    if rest or not years:
        parts.append(f"{rest} мес")
    return " ".join(parts)
